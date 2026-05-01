from rest_framework import serializers
from .models import Artwork

# class ArtworkSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Artwork
#         fields = '__all__'

class ArtworkSerializer(serializers.ModelSerializer):
    # Convert the ImageField to a string URL
    # Image = serializers.SerializerMethodField()

    class Meta:
        model = Artwork
        fields = [
            'Id', 'Title', 'Description', 'Artist', 'Image', 'Slug',
            'Likes', 'Saves', 'Views',
            'IsPublic', 'CreatedAt', 'UpdatedAt', 'CreatedBy', 'UpdatedBy'
        ]
        read_only_fields = ['Id', 'Likes', 'Saves', 'Views']

    def get_Image(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return self.context['request'].build_absolute_uri(obj.image.url)
        return None