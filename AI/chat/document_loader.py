"""
Document Loader — reads all .txt files from DOCUMENTS_DIR
and builds a combined knowledge base string for the AI.
"""
import os
from django.conf import settings

from pathlib import Path
from django.conf import settings

# def load_document(filename: str) -> str:
#     """Load a specific .txt document file."""

#     file_path = settings.DOCUMENTS_DIR / filename

#     print(f"[DocumentLoader] Loading file: {file_path}")

#     if not file_path.exists():
#         print(f"[DocumentLoader] File not found: {filename}")
#         return ""

#     try:
#         return file_path.read_text(encoding="utf-8")
#     except Exception as e:
#         print(f"[DocumentLoader] Error reading {filename}: {e}")
#         return ""

# def load_documents() -> str:
#     """Load all .txt document files and return combined text."""
#     docs_dir = settings.DOCUMENTS_DIR
#     print(f"[DocumentLoader] Loading documents from: {docs_dir}")
#     if not docs_dir.exists():
#         return ""

#     combined = []
#     for filename in sorted(docs_dir.iterdir()):
#         if filename.suffix == '.txt':
#             try:
#                 text = filename.read_text(encoding='utf-8')
#                 combined.append(f"=== FILE: {filename.name} ===\n{text}\n")
#             except Exception as e:
#                 print(f"[DocumentLoader] Could not read {filename}: {e}")

#     return "\n".join(combined)




def load_documents(filename: str | None = None) -> str:
    docs_dir = settings.DOCUMENTS_DIR

    if filename:
        file_path = docs_dir / filename
        print(f"[DocumentLoader] Loading documents from: {file_path}")
        return file_path.read_text(encoding="utf-8") if file_path.exists() else ""

    combined = []
    for file in sorted(docs_dir.iterdir()):
        if file.suffix == ".txt":
            combined.append(file.read_text(encoding="utf-8"))

    return "\n".join(combined)

# Cache at module level — documents are loaded once per server restart
_DOCUMENT_CACHE: str | None = None

""" Usage this load with filename 
text = load_document("business.txt")
text = load_document("agriculture.txt")

Later you should structure like:
documents/
   agriculture/
      farming.txt
      irrigation.txt
   business/
      services.txt
      pricing.txt

Then your AI can choose context dynamically.
""" 


def get_knowledge_base() -> str:
    global _DOCUMENT_CACHE
    if _DOCUMENT_CACHE is None:
        _DOCUMENT_CACHE = load_documents("document_loader.txt")
    return _DOCUMENT_CACHE


def reload_documents():
    """Force reload documents (call after uploading new files)."""
    global _DOCUMENT_CACHE
    _DOCUMENT_CACHE = None
    return get_knowledge_base()

