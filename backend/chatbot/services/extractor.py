import os
import re
from typing import List, Dict, Any
from django.conf import settings

try:
    import pypdf
except ImportError:
    pypdf = None

try:
    import docx
except ImportError:
    docx = None

class DocumentExtractionError(Exception):
    pass

class DocumentExtractor:
    @staticmethod
    def validate_and_extract(file_path: str, original_filename: str) -> Dict[str, Any]:
        """
        Validates file size, extension, magic bytes, and extracts text page-by-page.
        Returns:
            {
                'filename': str,
                'file_type': 'pdf' | 'docx' | 'txt',
                'file_size': int,
                'page_count': int,
                'full_text': str,
                'pages': [{'page_number': int, 'text': str, 'heading': str}]
            }
        """
        if not os.path.exists(file_path):
            raise DocumentExtractionError("File not found on server.")

        file_size = os.path.getsize(file_path)
        max_size_bytes = getattr(settings, 'MAX_UPLOAD_SIZE_MB', 20) * 1024 * 1024
        if file_size > max_size_bytes:
            raise DocumentExtractionError(
                f"File exceeds the maximum allowed size of {getattr(settings, 'MAX_UPLOAD_SIZE_MB', 20)} MB."
            )

        ext = os.path.splitext(original_filename)[1].lower().strip('.')
        if ext not in ['pdf', 'docx', 'txt', 'md']:
            raise DocumentExtractionError(f"Unsupported file format '.{ext}'. Supported formats: PDF, DOCX, TXT.")

        # Magic byte validation (FR-U-04 / TC-02)
        with open(file_path, 'rb') as f:
            header = f.read(2048)

        if ext == 'pdf':
            if not header.startswith(b'%PDF-'):
                raise DocumentExtractionError("File header mismatch: This file is not a valid PDF document (magic byte check failed).")
            return DocumentExtractor._extract_pdf(file_path, original_filename, file_size)

        elif ext == 'docx':
            if not header.startswith(b'PK\x03\x04'):
                raise DocumentExtractionError("File header mismatch: This file is not a valid DOCX document (magic byte check failed).")
            return DocumentExtractor._extract_docx(file_path, original_filename, file_size)

        elif ext in ['txt', 'md']:
            # Check if it looks like binary or text
            if b'\x00' in header:
                raise DocumentExtractionError("File appears to be a binary executable, not valid text.")
            return DocumentExtractor._extract_txt(file_path, original_filename, file_size)

        else:
            raise DocumentExtractionError(f"Unsupported file format: {ext}")

    @staticmethod
    def _extract_pdf(file_path: str, filename: str, file_size: int) -> Dict[str, Any]:
        if pypdf is None:
            raise DocumentExtractionError("PDF extraction library (pypdf) is not available.")

        try:
            reader = pypdf.PdfReader(file_path)
        except Exception as e:
            raise DocumentExtractionError(f"Corrupt or unreadable PDF: {str(e)}")

        page_count = len(reader.pages)
        max_pages = getattr(settings, 'MAX_PAGES', 100)
        if page_count > max_pages:
            raise DocumentExtractionError(
                f"Document has {page_count} pages, which exceeds the limit of {max_pages} pages."
            )

        pages = []
        full_text_parts = []
        heading_pattern = re.compile(r'^(?:[0-9]+(?:\.[0-9]+)*\s+[A-Za-z\s]+|[A-Z\s]{4,})$')

        for idx, page in enumerate(reader.pages, start=1):
            try:
                page_text = page.extract_text() or ""
            except Exception:
                page_text = ""

            page_text = page_text.strip()
            if page_text:
                full_text_parts.append(f"--- Page {idx} ---\n" + page_text)
                # Find the first prominent heading
                detected_heading = ""
                lines = page_text.splitlines()
                for line in lines[:8]:
                    line_clean = line.strip()
                    if heading_pattern.match(line_clean) and len(line_clean) < 60:
                        detected_heading = line_clean
                        break
                
                pages.append({
                    'page_number': idx,
                    'text': page_text,
                    'heading': detected_heading or f"Page {idx}"
                })

        full_text = "\n\n".join(full_text_parts)
        if not full_text.strip():
            raise DocumentExtractionError(
                "No extractable text found in this document. It may be an image-only or scanned document. "
                "Please upload a document with selectable text."
            )

        return {
            'filename': filename,
            'file_type': 'pdf',
            'file_size': file_size,
            'page_count': page_count,
            'full_text': full_text,
            'pages': pages
        }

    @staticmethod
    def _extract_docx(file_path: str, filename: str, file_size: int) -> Dict[str, Any]:
        if docx is None:
            raise DocumentExtractionError("DOCX extraction library (python-docx) is not available.")

        try:
            doc = docx.Document(file_path)
        except Exception as e:
            raise DocumentExtractionError(f"Corrupt or invalid DOCX document: {str(e)}")

        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        for table in doc.tables:
            for row in table.rows:
                row_text = " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                if row_text:
                    paragraphs.append(row_text)

        if not paragraphs:
            raise DocumentExtractionError("No extractable text found in this DOCX document.")

        full_text = "\n\n".join(paragraphs)
        # Approximate pages (~3000 chars per page)
        chars_per_page = 3000
        page_count = max(1, (len(full_text) // chars_per_page) + 1)
        max_pages = getattr(settings, 'MAX_PAGES', 100)
        if page_count > max_pages:
            raise DocumentExtractionError(f"Document exceeds the page limit of {max_pages} pages.")

        pages = []
        for i in range(page_count):
            start = i * chars_per_page
            end = start + chars_per_page
            page_content = full_text[start:end]
            pages.append({
                'page_number': i + 1,
                'text': page_content,
                'heading': f"Section {i+1}"
            })

        return {
            'filename': filename,
            'file_type': 'docx',
            'file_size': file_size,
            'page_count': page_count,
            'full_text': full_text,
            'pages': pages
        }

    @staticmethod
    def _extract_txt(file_path: str, filename: str, file_size: int) -> Dict[str, Any]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()

        content = content.strip()
        if not content:
            raise DocumentExtractionError("The uploaded text document is completely empty.")

        # Check for page breaks \f
        raw_pages = content.split('\f')
        if len(raw_pages) <= 1:
            chars_per_page = 3000
            page_count = max(1, (len(content) // chars_per_page) + 1)
            raw_pages = [content[i * chars_per_page : (i + 1) * chars_per_page] for i in range(page_count)]

        page_count = len(raw_pages)
        max_pages = getattr(settings, 'MAX_PAGES', 100)
        if page_count > max_pages:
            raise DocumentExtractionError(f"Document exceeds the page limit of {max_pages} pages.")

        pages = []
        for idx, page_content in enumerate(raw_pages, start=1):
            page_text = page_content.strip()
            if page_text:
                pages.append({
                    'page_number': idx,
                    'text': page_text,
                    'heading': f"Page {idx}"
                })

        return {
            'filename': filename,
            'file_type': 'txt',
            'file_size': file_size,
            'page_count': page_count,
            'full_text': content,
            'pages': pages
        }
