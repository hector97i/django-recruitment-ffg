from django.db import models
from image_app.storage_backends import PublicImagesStorage

# Create your models here.
class Image(models.Model):
    image = models.ImageField(storage=PublicImagesStorage())
