from django.shortcuts import render
from rest_framework import viewsets

from images.models import Image
from api.serializers import ImageSerializer

# add modelviewset for image
# implement searching in title
class ImageViewSet(viewsets.ModelViewSet):
    http_method_names = ('GET', 'POST', 'OPTIONS')
    queryset = Image.objects.all()
