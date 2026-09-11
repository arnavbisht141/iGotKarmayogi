import re
import json
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.models import TechnicalTranscript
from app.modules.technical_courses.schemas import (
    TranscriptIngestRequest, TranscriptChunk, TranscriptProcessResponse
)


class TranscriptService:
    """
    Service responsible for ingesting, cleaning, normalizing, and chunking
    technical-course video transcripts and lecture notes.
    """

    @staticmethod
    def clean_transcript(raw_text: str) -> str:
        """
        Cleans subtitle timestamps (VTT/SRT format), audio cues [Music],
        and excessive whitespace while preserving technical terms and punctuation.
        """
        if not raw_text:
            return ""

        # Remove WebVTT / SRT header
        text = re.sub(r'WEBVTT.*?\n', '', raw_text, flags=re.IGNORECASE)
        # Remove timestamp lines like 00:00:00.000 --> 00:00:04.000 or 00:01,234 --> 00:01,567
        text = re.sub(r'\d{1,2}:\d{2}(?::\d{2})?(?:[.,]\d{3})?\s*-->\s*\d{1,2}:\d{2}(?::\d{2})?(?:[.,]\d{3})?', '', text)
        # Remove standalone index numbers
        text = re.sub(r'^\s*\d+\s*$', '', text, flags=re.MULTILINE)
        # Remove bracketed audio tags like [Applause], [Music], (laughter)
        text = re.sub(r'\[.*?\]|\(.*?\)', '', text)
        # Normalize whitespace and newlines
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n\s*\n+', '\n\n', text)
        return text.strip()

    @staticmethod
    def estimate_tokens(text: str) -> int:
        """Heuristic estimation of tokens (approx 4 chars per token)."""
        return max(1, len(text) // 4)

    @staticmethod
    def chunk_transcript(
        cleaned_text: str,
        chunk_size_chars: int = 1500,
        overlap_chars: int = 200
    ) -> List[TranscriptChunk]:
        """
        Splits cleaned text into overlapping semantic chunks for LLM processing.
        """
        if not cleaned_text:
            return []

        chunks: List[TranscriptChunk] = []
        start = 0
        text_len = len(cleaned_text)
        chunk_idx = 0

        while start < text_len:
            end = min(start + chunk_size_chars, text_len)
            
            # If not at the very end, try to break at a paragraph or sentence boundary
            if end < text_len:
                boundary = cleaned_text.rfind('\n\n', start, end)
                if boundary == -1 or boundary <= start:
                    boundary = cleaned_text.rfind('. ', start, end)
                if boundary > start:
                    end = boundary + 1

            chunk_str = cleaned_text[start:end].strip()
            if chunk_str:
                token_count = TranscriptService.estimate_tokens(chunk_str)
                chunks.append(
                    TranscriptChunk(
                        chunk_index=chunk_idx,
                        text=chunk_str,
                        token_count=token_count,
                        start_char=start,
                        end_char=end,
                        metadata={
                            "chunk_index": chunk_idx,
                            "estimated_tokens": token_count
                        }
                    )
                )
                chunk_idx += 1

            if end >= text_len:
                break
            start = max(end - overlap_chars, start + 1)

        return chunks

    @classmethod
    def process_and_persist(
        cls,
        req: TranscriptIngestRequest,
        db: Optional[Session] = None
    ) -> TranscriptProcessResponse:
        """
        Cleans, chunks, and optionally saves the transcript to the database.
        """
        cleaned = cls.clean_transcript(req.raw_text)
        chunks = cls.chunk_transcript(cleaned)
        total_tokens = sum(c.token_count for c in chunks)

        transcript_record_id = None
        if db is not None:
            chunks_data = [c.model_dump() for c in chunks]
            record = TechnicalTranscript(
                course_id=req.course_id,
                title=req.title,
                raw_text=req.raw_text,
                cleaned_text=cleaned,
                chunks_json=json.dumps(chunks_data),
                metadata_json=json.dumps(req.metadata or {})
            )
            db.add(record)
            db.commit()
            db.refresh(record)
            transcript_record_id = record.id

        return TranscriptProcessResponse(
            id=transcript_record_id,
            title=req.title,
            course_id=req.course_id,
            cleaned_length=len(cleaned),
            estimated_tokens=total_tokens,
            chunk_count=len(chunks),
            chunks=chunks,
            metadata=req.metadata or {}
        )
