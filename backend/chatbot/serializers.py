from rest_framework import serializers
from .models import ChatSession, Document, Chunk, Message

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            'id', 'session', 'filename', 'file_type', 'file_size',
            'page_count', 'status', 'error_message', 'uploaded_at'
        ]

class ChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chunk
        fields = ['id', 'chunk_index', 'page_number', 'heading', 'text']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'session', 'role', 'content', 'sources', 'created_at']

class ChatSessionSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = ['id', 'created_at', 'last_active_at', 'documents', 'messages']
