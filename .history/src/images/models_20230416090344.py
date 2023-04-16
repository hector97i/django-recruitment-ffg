from django.db import models
from image_app.storage_backends import PublicImagesStorage

# Create your models here.
class Image(models.Model):
    name = models.CharField(max_length=256)
    image = models.ImageField(
        max_length=1024 * 1000 * 10,
        height_field='height',
        width_field='width',
        storage=PublicImagesStorage(),
    )
    height = models.PositiveIntegerField()
    width = models.PositiveIntegerField()
