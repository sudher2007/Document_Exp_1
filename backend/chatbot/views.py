import os
import uuid
from pathlib import Path
from django.conf import settings
from django.http import FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import ChatSession, Document, Chunk, Message
from .serializers import DocumentSerializer, MessageSerializer
from .services.extractor import DocumentExtractor, DocumentExtractionError
from .services.chunker import DocumentChunker
from .services.rag_engine import RAGEngine, REFUSAL_INFO_NOT_FOUND, REFUSAL_UNRELATED_QUESTION, SRS_SYSTEM_PROMPT


class DocumentUploadView(APIView):
    """
    POST /api/documents/
    Upload any PDF, DOCX, or TXT document, extract text, chunk and index for RAG.
    """
    def post(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get('file')
        session_id = request.data.get('session_id')

        if not uploaded_file:
            return Response({'error': 'No file was provided.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get or create session
        if not session_id:
            session = ChatSession.objects.create()
        else:
            session, _ = ChatSession.objects.get_or_create(id=session_id)

        # Replace flag: wipe existing docs + messages for this session
        replace = request.data.get('replace', 'false').lower() == 'true'
        if replace:
            Document.objects.filter(session=session).delete()
            Message.objects.filter(session=session).delete()

        # Save uploaded file to media/
        media_dir = Path(settings.MEDIA_ROOT)
        media_dir.mkdir(parents=True, exist_ok=True)
        safe_name = f"{uuid.uuid4().hex}_{uploaded_file.name}"
        saved_path = media_dir / safe_name

        with open(saved_path, 'wb+') as dest:
            for chunk in uploaded_file.chunks():
                dest.write(chunk)

        doc = Document.objects.create(
            session=session,
            filename=uploaded_file.name,
            file_type=uploaded_file.name.split('.')[-1].lower(),
            file_size=uploaded_file.size,
            file_path=str(saved_path),
            status='processing'
        )

        try:
            extracted = DocumentExtractor.validate_and_extract(str(saved_path), uploaded_file.name)
            doc.page_count = extracted['page_count']
            doc.full_text = extracted['full_text']
            doc.file_type = extracted['file_type']
            doc.status = 'ready'
            doc.save()

            chunks_data = DocumentChunker.chunk_document(extracted['pages'])
            Chunk.objects.bulk_create([
                Chunk(
                    document=doc,
                    chunk_index=ch['chunk_index'],
                    page_number=ch['page_number'],
                    heading=ch['heading'],
                    text=ch['text']
                ) for ch in chunks_data
            ])

            return Response({
                'message': f'"{uploaded_file.name}" uploaded, extracted, and indexed successfully.',
                'document': DocumentSerializer(doc).data,
                'session_id': str(session.id),
                'chunk_count': len(chunks_data)
            }, status=status.HTTP_201_CREATED)

        except DocumentExtractionError as e:
            doc.status = 'error'
            doc.error_message = str(e)
            doc.save()
            return Response({'error': str(e), 'document': DocumentSerializer(doc).data},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            doc.status = 'error'
            doc.error_message = f"Unexpected error: {str(e)}"
            doc.save()
            return Response({'error': doc.error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DocumentDetailView(APIView):
    """
    GET  /api/documents/<id>/  — status
    DELETE /api/documents/<id>/ — remove
    """
    def get(self, request, pk, *args, **kwargs):
        try:
            doc = Document.objects.get(pk=pk)
            return Response({'document': DocumentSerializer(doc).data, 'chunk_count': doc.chunks.count()})
        except Document.DoesNotExist:
            return Response({'error': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, *args, **kwargs):
        try:
            doc = Document.objects.get(pk=pk)
            if doc.file_path and os.path.exists(doc.file_path):
                try:
                    os.remove(doc.file_path)
                except Exception:
                    pass
            doc.delete()
            return Response({'message': 'Document deleted.'})
        except Document.DoesNotExist:
            return Response({'error': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)


class DocumentActionsView(APIView):
    """
    POST /api/documents/<id>/actions/
    One-click document actions: summarize | keypoints | entities | outline
    Body: { "action": "summarize" | "keypoints" | "entities" | "outline", "api_key": "..." }
    """
    ACTION_LABELS = {
        'summarize': 'Summary',
        'keypoints': 'Key Points',
        'entities':  'Named Entities',
        'outline':   'Document Outline',
    }
    ACTION_QUERIES = {
        'summarize': 'Summarize this document comprehensively.',
        'keypoints': 'What are the main key points of this document?',
        'entities':  'Extract all named entities from this document.',
        'outline':   'Provide a structured outline of this document.',
    }

    def post(self, request, pk, *args, **kwargs):
        action = request.data.get('action', 'summarize').lower()
        custom_api_key = request.data.get('api_key', '').strip()
        session_id = request.data.get('session_id', '')

        if action not in self.ACTION_LABELS:
            return Response(
                {'error': f"Unknown action '{action}'. Choose from: {list(self.ACTION_LABELS.keys())}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            doc = Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            return Response({'error': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)

        if doc.status != 'ready':
            return Response(
                {'error': f'Document is not ready (current status: {doc.status}).'},
                status=status.HTTP_400_BAD_REQUEST
            )

        chunks = list(doc.chunks.all())
        rag = RAGEngine()
        result = rag.answer_question(
            query=self.ACTION_QUERIES[action],
            document_chunks=chunks,
            full_document_text=doc.full_text,
            custom_api_key=custom_api_key,
            action=action
        )

        # Optionally persist as a message in the session
        if session_id:
            try:
                session = ChatSession.objects.get(id=session_id)
                Message.objects.create(session=session, role='user', content=self.ACTION_QUERIES[action])
                Message.objects.create(
                    session=session, role='assistant',
                    content=result['answer'], sources=result['sources']
                )
            except ChatSession.DoesNotExist:
                pass

        return Response({
            'action': action,
            'label': self.ACTION_LABELS[action],
            'answer': result['answer'],
            'sources': result['sources'],
            'engine': result['engine'],
            'document': {'id': str(doc.id), 'filename': doc.filename, 'page_count': doc.page_count}
        })


class ChatView(APIView):
    """
    POST /api/chat/
    Send a question and receive a document-grounded answer.
    Works for any document, not just the college policy.
    """
    def post(self, request, *args, **kwargs):
        session_id = request.data.get('session_id')
        query = request.data.get('query', '').strip()
        custom_api_key = request.data.get('api_key', '').strip()

        if not session_id:
            return Response({'error': 'session_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        max_chars = getattr(settings, 'MAX_MESSAGE_CHARS', 2000)
        if len(query) > max_chars:
            return Response(
                {'error': f'Message exceeds the {max_chars}-character limit.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not query:
            return Response({'error': 'Question cannot be empty.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            session = ChatSession.objects.get(id=session_id)
        except ChatSession.DoesNotExist:
            return Response({'error': 'Invalid or expired session.'}, status=status.HTTP_404_NOT_FOUND)

        ready_docs = session.documents.filter(status='ready')
        if not ready_docs.exists():
            return Response(
                {'error': 'No document is ready. Please upload or load a document first.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        active_doc = ready_docs.latest('uploaded_at')
        chunks = list(active_doc.chunks.all())

        # Conversation history (last 10 turns)
        recent = list(session.messages.order_by('-created_at')[:10])
        recent.reverse()
        history = [{'role': m.role, 'content': m.content} for m in recent]

        Message.objects.create(session=session, role='user', content=query)

        rag = RAGEngine()
        result = rag.answer_question(
            query=query,
            document_chunks=chunks,
            full_document_text=active_doc.full_text,
            conversation_history=history,
            custom_api_key=custom_api_key,
        )

        assistant_msg = Message.objects.create(
            session=session, role='assistant',
            content=result['answer'], sources=result['sources']
        )

        return Response({
            'message_id': assistant_msg.id,
            'answer': result['answer'],
            'sources': result['sources'],
            'grounded': result['grounded'],
            'declined': result['declined'],
            'engine': result['engine'],
            'document': {
                'id': str(active_doc.id),
                'filename': active_doc.filename,
                'page_count': active_doc.page_count
            }
        })


class ChatHistoryView(APIView):
    """
    GET    /api/chat/<session_id>/history/  — fetch history
    DELETE /api/chat/<session_id>/          — clear messages (keep document)
    """
    def get(self, request, session_id, *args, **kwargs):
        try:
            session = ChatSession.objects.get(id=session_id)
            return Response({
                'session_id': session.id,
                'messages': MessageSerializer(session.messages.order_by('created_at'), many=True).data
            })
        except ChatSession.DoesNotExist:
            return Response({'error': 'Session not found.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, session_id, *args, **kwargs):
        try:
            session = ChatSession.objects.get(id=session_id)
            session.messages.all().delete()
            return Response({'message': 'Conversation cleared.'})
        except ChatSession.DoesNotExist:
            return Response({'error': 'Session not found.'}, status=status.HTTP_404_NOT_FOUND)


class LoadCollegePolicyView(APIView):
    """
    POST /api/load-policy-pdf/
    Load and index the built-in Meridian College Policy Manual PDF.
    """
    def post(self, request, *args, **kwargs):
        session_id = request.data.get('session_id')
        if not session_id:
            session = ChatSession.objects.create()
        else:
            session, _ = ChatSession.objects.get_or_create(id=session_id)

        Document.objects.filter(session=session).delete()
        Message.objects.filter(session=session).delete()

        pdf_path = Path(settings.BASE_DIR) / 'meridian_college_policy_manual.pdf'
        if not pdf_path.exists():
            import sys
            sys.path.insert(0, str(settings.BASE_DIR))
            from generate_policy_pdf import generate_policy_pdf
            generate_policy_pdf(str(pdf_path))

        extracted = DocumentExtractor.validate_and_extract(str(pdf_path), 'meridian_college_policy_manual.pdf')
        doc = Document.objects.create(
            session=session,
            filename='Meridian College Policy Manual (First Edition 2026-27).pdf',
            file_type='pdf',
            file_size=pdf_path.stat().st_size,
            page_count=extracted['page_count'],
            full_text=extracted['full_text'],
            file_path=str(pdf_path),
            status='ready'
        )
        chunks_data = DocumentChunker.chunk_document(extracted['pages'])
        Chunk.objects.bulk_create([
            Chunk(document=doc, chunk_index=ch['chunk_index'],
                  page_number=ch['page_number'], heading=ch['heading'], text=ch['text'])
            for ch in chunks_data
        ])

        return Response({
            'message': 'Meridian College Policy Manual loaded and indexed for RAG.',
            'document': DocumentSerializer(doc).data,
            'session_id': str(session.id),
            'chunk_count': len(chunks_data),
        }, status=status.HTTP_201_CREATED)


class DownloadCollegePolicyView(APIView):
    """GET /api/download-policy-pdf/"""
    def get(self, request, *args, **kwargs):
        pdf_path = Path(settings.BASE_DIR) / 'meridian_college_policy_manual.pdf'
        if not pdf_path.exists():
            import sys
            sys.path.insert(0, str(settings.BASE_DIR))
            from generate_policy_pdf import generate_policy_pdf
            generate_policy_pdf(str(pdf_path))
        return FileResponse(open(pdf_path, 'rb'), as_attachment=True,
                            filename='meridian_college_policy_manual.pdf')


class SettingsConfigView(APIView):
    """GET / POST /api/settings/"""
    def get(self, request, *args, **kwargs):
        active_key = getattr(settings, 'GEMINI_API_KEY', '') or os.environ.get('GEMINI_API_KEY', '')
        return Response({
            'has_api_key': bool(active_key),
            'api_key_masked': (active_key[:4] + '...' + active_key[-4:]) if len(active_key) >= 8 else '',
            'model_name': getattr(settings, 'GEMINI_MODEL', 'gemini-2.5-flash'),
            'temperature': getattr(settings, 'GEMINI_TEMPERATURE', 0.2),
            'system_prompt': SRS_SYSTEM_PROMPT,
            'max_message_chars': getattr(settings, 'MAX_MESSAGE_CHARS', 2000),
            'max_upload_size_mb': getattr(settings, 'MAX_UPLOAD_SIZE_MB', 20),
            'refusals': {
                'info_not_found': REFUSAL_INFO_NOT_FOUND,
                'unrelated_question': REFUSAL_UNRELATED_QUESTION
            }
        })

    def post(self, request, *args, **kwargs):
        new_key = request.data.get('api_key', '').strip()
        model_name = request.data.get('model_name', '').strip()
        temperature = request.data.get('temperature')

        if new_key:
            settings.GEMINI_API_KEY = new_key
            os.environ['GEMINI_API_KEY'] = new_key
        if model_name:
            settings.GEMINI_MODEL = model_name
        if temperature is not None:
            settings.GEMINI_TEMPERATURE = float(temperature)

        return Response({
            'message': 'Configuration updated.',
            'has_api_key': bool(getattr(settings, 'GEMINI_API_KEY', '')),
            'model_name': getattr(settings, 'GEMINI_MODEL', 'gemini-2.5-flash'),
            'temperature': getattr(settings, 'GEMINI_TEMPERATURE', 0.2)
        })
