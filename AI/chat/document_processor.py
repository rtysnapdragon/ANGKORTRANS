import hashlib
import json
import re
from typing import List, Dict, Any
from django.db import transaction
from ..models import AI_DOCUMENTS, AI_DOCUMENT_CHUNKS, AI_QUERY_LOGS

class DocumentProcessor:
    """Handle document processing, chunking, and retrieval"""
    
    def __init__(self, chunk_size=500, overlap=50):
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.overlap):
            chunk_words = words[i:i + self.chunk_size]
            if chunk_words:
                chunks.append(' '.join(chunk_words))
        
        return chunks
    
    def process_document(self, document_data: Dict) -> AI_DOCUMENTS:
        """Process and store a document with chunks"""
        with transaction.atomic():
            # Create or update document
            content_hash = hashlib.sha256(document_data['CONTENT'].encode()).hexdigest()
            
            document, created = AI_DOCUMENTS.objects.update_or_create(
                CONTENT_HASH=content_hash,
                defaults={
                    'TITLE': document_data['TITLE'],
                    'CONTENT': document_data['CONTENT'],
                    'SUMMARY': document_data.get('SUMMARY', ''),
                    'DOCUMENT_TYPE': document_data.get('DOCUMENT_TYPE', 'ARTICLE'),
                    'CATEGORY': document_data.get('CATEGORY'),
                    'TAGS': document_data.get('TAGS', []),
                    'LANGUAGE': document_data.get('LANGUAGE', 'EN'),
                    'METADATA': document_data.get('METADATA', {}),
                }
            )
            
            # Delete existing chunks
            AI_DOCUMENT_CHUNKS.objects.filter(DOCUMENT=document).delete()
            
            # Create new chunks
            chunks = self.chunk_text(document.CONTENT)
            for idx, chunk_content in enumerate(chunks):
                AI_DOCUMENT_CHUNKS.objects.create(
                    DOCUMENT=document,
                    CHUNK_INDEX=idx,
                    CONTENT=chunk_content,
                    TOKEN_COUNT=len(chunk_content.split())
                )
            
            return document
    
    def search_documents(self, query: str, language: str = 'EN', 
                        categories: List[str] = None, limit: int = 5) -> List[Dict]:
        """Search for relevant documents using keyword matching"""
        from django.db.models import Q
        
        # Build search query
        search_terms = query.split()
        q_objects = Q()
        
        for term in search_terms:
            if len(term) > 2:  # Ignore short terms
                q_objects |= Q(TITLE__icontains=term)
                q_objects |= Q(CONTENT__icontains=term)
                q_objects |= Q(CATEGORY__icontains=term)
        
        # Filter by language and active status
        documents = AI_DOCUMENTS.objects.filter(
            IS_ACTIVE=True,
            LANGUAGE=language
        ).filter(q_objects)
        
        # Filter by categories if specified
        if categories:
            documents = documents.filter(CATEGORY__in=categories)
        
        # Calculate relevance score (simple version)
        results = []
        for doc in documents[:limit]:
            relevance_score = self._calculate_relevance(doc, query)
            results.append({
                'id': doc.ID,
                'title': doc.TITLE,
                'content': doc.CONTENT[:1000],  # Preview
                'full_content': doc.CONTENT,
                'category': doc.CATEGORY,
                'document_type': doc.DOCUMENT_TYPE,
                'relevance_score': relevance_score,
                'chunks': doc.chunks.all().values('CHUNK_INDEX', 'CONTENT')
            })
        
        return sorted(results, key=lambda x: x['relevance_score'], reverse=True)
    
    def _calculate_relevance(self, document: AI_DOCUMENTS, query: str) -> float:
        """Calculate simple relevance score"""
        query_terms = set(query.lower().split())
        title_terms = set(document.TITLE.lower().split())
        content_lower = document.CONTENT.lower()
        
        # Title matches (weight: 0.4)
        title_match = len(query_terms.intersection(title_terms)) / max(len(query_terms), 1)
        
        # Content matches (weight: 0.6)
        content_matches = sum(1 for term in query_terms if term in content_lower)
        content_score = content_matches / max(len(query_terms), 1)
        
        return (title_match * 0.4) + (content_score * 0.6)
    
    def get_relevant_chunks(self, query: str, language: str = 'EN', limit: int = 10) -> List[Dict]:
        """Retrieve most relevant document chunks"""
        from django.db.models import Q
        
        search_terms = query.split()
        q_objects = Q(CONTENT__icontains=query)
        
        for term in search_terms:
            if len(term) > 2:
                q_objects |= Q(CONTENT__icontains=term)
        
        chunks = AI_DOCUMENT_CHUNKS.objects.filter(
            DOCUMENT__IS_ACTIVE=True,
            DOCUMENT__LANGUAGE=language
        ).filter(q_objects).select_related('DOCUMENT')[:limit]
        
        results = []
        for chunk in chunks:
            results.append({
                'chunk_id': chunk.ID,
                'document_title': chunk.DOCUMENT.TITLE,
                'content': chunk.CONTENT,
                'chunk_index': chunk.CHUNK_INDEX,
                'document_type': chunk.DOCUMENT.DOCUMENT_TYPE
            })
        
        return results

class DocumentQueryService:
    """Service for querying documents with AI"""
    
    def __init__(self):
        self.processor = DocumentProcessor()
    
    def build_context_from_documents(self, query: str, language: str = 'EN') -> str:
        """Build context string from relevant documents"""
        # Get relevant chunks
        chunks = self.processor.get_relevant_chunks(query, language, limit=5)
        
        if not chunks:
            return ""
        
        context_parts = ["Here is relevant information from RamaGallery's knowledge base:\n"]
        
        for chunk in chunks:
            context_parts.append(f"[From: {chunk['document_title']}]")
            context_parts.append(chunk['content'])
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    def search_documents_api(self, query: str, language: str = 'EN', 
                            category: str = None, limit: int = 10) -> Dict:
        """API endpoint to search documents"""
        categories = [category] if category else None
        documents = self.processor.search_documents(query, language, categories, limit)
        
        return {
            'success': True,
            'query': query,
            'language': language,
            'results': documents,
            'total_found': len(documents)
        }