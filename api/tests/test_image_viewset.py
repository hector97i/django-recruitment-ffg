import os

from rest_framework.test import APITestCase

from images.models import Image
from parameterized import parameterized

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))
)

names = [
    ('alpha', 3),
    ('bravo', 5),
    ('charlie', 9),
    ('delta', 10),
]

class TestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.images = {n[0]: [] for n in names}
        for name_data in names:
            name, quantity = name_data
            for n in range(quantity):
                img_obj = Image.objects.create(
                    title=f'lenna_{name}_{n + 1}.png',
                )
                cls.images[name].append(img_obj)

    @parameterized.expand(names)
    def test_search_images(self, name, quantity):
        response = self.client.get(f'/api/images/?search={name}')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['results']), quantity)

    def test_post_image(self):
        response = self.client.post(
            '/api/images/?width=200&height=599',
            data={'title': 'test_lenna', 'image': open(os.path.join(__location__, 'lenna.png'), 'rb')},
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data['width'], 200)
        self.assertEqual(data['height'], 599)
