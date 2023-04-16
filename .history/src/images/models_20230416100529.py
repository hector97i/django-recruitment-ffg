from django.db import models
from image_app.storage_backends import PublicImagesStorage

class Image(models.Model):
    title = models.CharField(max_length=256)
    url = models.ImageField(
        # maximum 5MB
        max_length=1024 * 1000 * 5,
        height_field='height',
        width_field='width',
        storage=PublicImagesStorage(),
    )
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return f'[IMAGE]: "{self.title}" {self.width} x {self.height}'
