from rest_framework import routers

from api.views import ImageViewSet

router = routers.SimpleRouter()
router.register('images', ImageViewSet, 'images')

urlpatterns = [] + router.urls
