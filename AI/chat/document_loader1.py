from pathlib import Path
from django.conf import settings

def detect_domain(query: str) -> str:
    q = query.lower()

    if any(k in q for k in ["farm", "crop", "soil", "rice", "agriculture","document_loader"]):
        return "agriculture"

    if any(k in q for k in ["price", "service", "cost", "plan", "business","TechFlow Solutions"]):
        return "business"

    return "general"

def load_document(domain: str, filename: str) -> str:
    """
    Load a specific document from domain folder.
    Example:
        load_document("agriculture", "farming.txt")
    """

    file_path = settings.DOCUMENTS_DIR / domain / filename

    print(f"[DocumentLoader] Loading: {file_path}")

    if not file_path.exists():
        print(f"[DocumentLoader] Not found: {file_path}")
        return ""

    return file_path.read_text(encoding="utf-8")


def load_domain(domain: str) -> str:
    """
    Load all documents inside a domain folder.
    Example: agriculture/
    """

    folder = settings.DOCUMENTS_DIR / domain

    if not folder.exists():
        return ""

    combined = []

    for file in sorted(folder.glob("*.txt")):
        try:
            text = file.read_text(encoding="utf-8")
            combined.append(f"=== {file.name} ===\n{text}")
        except Exception as e:
            print(f"[DocumentLoader] Error {file}: {e}")

    return "\n\n".join(combined)