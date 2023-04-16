import logging
import os
from io import BytesIO

import pytest
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image as PilImage

from images.models import Image

logger = logging.getLogger(__name__)

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

@pytest.mark.parametrize(
    'width, height',
    [
        (100, 200),
        (1000, 300),
        (3000, 300)
    ],
)
def test_image_rezise(width, height):
    with open(os.path.join(__location__, 'lenna.png'), 'rb') as image_file:
        in_mem = InMemoryUploadedFile(image_file, None, 'lenna.png', 'image/png', None, None)
        resized = Image.resize_image(in_mem, width, height)
        memory_image = BytesIO(resized.read())
        pil_image = PilImage.open(memory_image)
        assert pil_image.size == (width, height)
