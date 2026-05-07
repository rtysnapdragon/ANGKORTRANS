import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ANGKORTRANS.settings')
django.setup()

from AI.chat.models import AI_DOCUMENTS

documents = [
    {
        'TITLE': 'RamaGallery Art Collection 2024',
        'CONTENT': 'RamaGallery features contemporary Khmer art including traditional Apsara dance paintings, modern abstract works, and mixed media installations...',
        'CATEGORY': 'ARTWORKS',
        'LANGUAGE': 'EN'
    },
    {
        'TITLE': 'របៀបទស្សនាវិចិត្រសាល',
        'CONTENT': 'វិចិត្រសាលរាមារ៉ាបើកពីម៉ោង ៩ព្រឹក ដល់ ៦ល្ងាច ថ្ងៃចន្ទ ដល់ សៅរ៍...',
        'CATEGORY': 'INFORMATION',
        'LANGUAGE': 'KM'
    }
]

for doc in documents:
    AI_DOCUMENTS.objects.create(**doc)
    print(f"Loaded: {doc['TITLE']}")