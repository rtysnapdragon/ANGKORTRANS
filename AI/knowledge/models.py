from django.db import models

class KnowledgeDocument(models.Model):

    LANGUAGE_CHOICES = (
        ("en", "English"),
        ("km", "Khmer"),
    )

    title = models.CharField(max_length=255)

    slug = models.SlugField(unique=True)

    content = models.TextField()

    category = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    tags = models.JSONField(
        default=list,
        blank=True
    )

    language = models.CharField(
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default="en"
    )

    priority = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "KNOWLEDGE_DOCUMENTS"
        ordering = ["-priority", "-updated_at"]

    def __str__(self):
        return self.title