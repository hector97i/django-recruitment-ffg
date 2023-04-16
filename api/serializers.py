from rest_framework import serializers
from images.models import Image
# create serializer for Image that validates:
# - file format allowed
# - validate size no larger than 5MB
class ImageSerializer(serializers.ModelSerializer):
    url = serializers.ImageField(source='image')

    class Meta:
        model = Image
        fields = (
            'id',
            'title',
            'url',
            'width',
            'height',
        )

class ImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = (
            'id',
            'title',
            'image',
        )
