# from knowledge.models import KnowledgeDocument

# def search_documents(query):

#     return KnowledgeDocument.objects.raw("""
#         SELECT *
#         FROM KNOWLEDGE_DOCUMENTS
#         WHERE MATCH(TITLE, CONTENT)
#         AGAINST(%s)
#         LIMIT 5
#     """, [query])

from django.db import connection
from AI.knowledge.models import KnowledgeDocument


def search_documents(query, limit=5):

    sql = """
    SELECT *
    FROM KNOWLEDGE_DOCUMENTS
    WHERE MATCH(title, content)
    AGAINST(%s IN NATURAL LANGUAGE MODE)
    AND is_active = 1
    LIMIT %s
    """

    return KnowledgeDocument.objects.raw(
        sql,
        [query, limit]
    )