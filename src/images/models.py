import os
from io import BytesIO

from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from django.db import models
from PIL import Image as PilImage

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
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return f'[IMAGE]: "{self.title}" - {self.width}px x {self.height}px'

    @staticmethod
    def resize_image(image, width, height):
        # There are 2 situations: the file is smaller than or greater than 2.5MB
        # https://docs.djangoproject.com/en/3.2/topics/http/file-uploads/#where-uploaded-data-is-stored

        new_size = (int(width), int(height))
        if isinstance(image, InMemoryUploadedFile):
            # if it is smaller than 2.5MB, django uses InMemoryUploadedFile
            memory_image = BytesIO(image.read())
            pil_image = PilImage.open(memory_image)
            img_format = os.path.splitext(image.name)[1][1:].upper()
            img_format = 'JPEG' if img_format == 'JPG' else img_format
            # resize returns a new copy of the image
            pil_image = pil_image.resize(new_size)

            new_image = BytesIO()
            pil_image.save(new_image, format=img_format)

            new_image = ContentFile(new_image.getvalue())
            image = InMemoryUploadedFile(new_image, None, image.name, image.content_type, None, None)
        elif isinstance(image, TemporaryUploadedFile):
            # if it is greater than 2.5MB, django uses TemporaryUploadedFile
            path = image.temporary_file_path()
            pil_image = PilImage.open(path)
            pil_image = pil_image.resize(new_size)
            pil_image.save(path)
            image.size = os.stat(path).st_size

        return image
