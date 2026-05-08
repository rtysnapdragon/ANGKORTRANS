from django.contrib import admin

from apps.knowledge.models import (
    KnowledgeDocument
)

@admin.register(KnowledgeDocument)
class KnowledgeDocumentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "category",
        "language",
        "priority",
        "is_active",
        "updated_at"
    )

    search_fields = (
        "title",
        "content"
    )

    list_filter = (
        "language",
        "category",
        "is_active"
    )

    prepopulated_fields = {
        "slug": ("title",)
    }