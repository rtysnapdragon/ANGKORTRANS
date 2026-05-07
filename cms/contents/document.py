from django_opensearch_dsl import Document
from django_opensearch_dsl.registries import registry

from .models import Content

@registry.register_document
class ContentDocument(Document):

    class Index:
        name = 'ramagallery_contents'

    class Django:
        model = Content

        fields = [
            'ID',
            'TITLE',
            'DESCRIPTION',
            'CONTENT_TYPE',
            'VIEW_COUNT',
            'CREATED_AT'
        ]