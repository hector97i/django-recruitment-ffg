from django.db import models
from image_app.storage_backends import PublicImagesStorage

class Image(models.Model):
    title = models.CharField(max_length=256)
    image = models.ImageField(
        # maximum 5MB
        max_length=1024 * 1000 * 5,
        height_field='height',
        width_field='width',
        storage=PublicImagesStorage(),
    )
    width = models.PositiveIntegerField()
    height = models.PositiveIntegerField()
