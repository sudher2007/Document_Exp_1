import re
from typing import List, Dict, Any

class DocumentChunker:
    CHUNK_SIZE = 2200 # roughly 500-600 tokens
    CHUNK_OVERLAP = 300 # roughly 10-15%

    @classmethod
    def chunk_document(cls, pages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Takes list of extracted page dicts: [{'page_number': int, 'text': str, 'heading': str}]
        Returns list of chunks:
        [
            {
                'chunk_index': int,
                'page_number': int,
                'heading': str,
                'text': str
            }
        ]
        """
        chunks = []
        chunk_idx = 0

        heading_re = re.compile(r'^(?:[0-9]+(?:\.[0-9]+)*\s+[A-Za-z\s]+|[A-Z\s]{4,})$')

        for page in pages:
            page_num = page['page_number']
            page_text = page['text'].strip()
            page_heading = page.get('heading', f"Page {page_num}")

            if not page_text:
                continue

            # If page text is within chunk size, keep it as a clean single chunk
            if len(page_text) <= cls.CHUNK_SIZE:
                chunks.append({
                    'chunk_index': chunk_idx,
                    'page_number': page_num,
                    'heading': page_heading,
                    'text': page_text
                })
                chunk_idx += 1
                continue

            # If larger, split along paragraph boundaries (\n\n or \n)
            paragraphs = [p.strip() for p in page_text.split('\n\n') if p.strip()]
            current_chunk = []
            current_len = 0
            current_heading = page_heading

            for para in paragraphs:
                # Check if paragraph looks like a heading
                lines = para.splitlines()
                if lines and heading_re.match(lines[0].strip()) and len(lines[0].strip()) < 60:
                    current_heading = lines[0].strip()

                para_len = len(para)
                if current_len + para_len <= cls.CHUNK_SIZE:
                    current_chunk.append(para)
                    current_len += para_len + 2
                else:
                    if current_chunk:
                        chunk_text = "\n\n".join(current_chunk)
                        chunks.append({
                            'chunk_index': chunk_idx,
                            'page_number': page_num,
                            'heading': current_heading,
                            'text': chunk_text
                        })
                        chunk_idx += 1

                        # Keep overlap from the end of the current chunk
                        overlap_text = chunk_text[-cls.CHUNK_OVERLAP:] if len(chunk_text) > cls.CHUNK_OVERLAP else ""
                        current_chunk = [overlap_text, para] if overlap_text else [para]
                        current_len = len(overlap_text) + para_len
                    else:
                        # Paragraph itself is larger than CHUNK_SIZE: split by sentences
                        sentences = re.split(r'(?<=[.!?])\s+', para)
                        sub_chunk = []
                        sub_len = 0
                        for sent in sentences:
                            if sub_len + len(sent) <= cls.CHUNK_SIZE:
                                sub_chunk.append(sent)
                                sub_len += len(sent) + 1
                            else:
                                if sub_chunk:
                                    chunks.append({
                                        'chunk_index': chunk_idx,
                                        'page_number': page_num,
                                        'heading': current_heading,
                                        'text': " ".join(sub_chunk)
                                    })
                                    chunk_idx += 1
                                sub_chunk = [sent]
                                sub_len = len(sent)
                        if sub_chunk:
                            chunks.append({
                                'chunk_index': chunk_idx,
                                'page_number': page_num,
                                'heading': current_heading,
                                'text': " ".join(sub_chunk)
                            })
                            chunk_idx += 1
                        current_chunk = []
                        current_len = 0

            if current_chunk:
                chunks.append({
                    'chunk_index': chunk_idx,
                    'page_number': page_num,
                    'heading': current_heading,
                    'text': "\n\n".join(current_chunk)
                })
                chunk_idx += 1

        return chunks
