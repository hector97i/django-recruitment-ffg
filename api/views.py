import logging

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from images.models import Image
from rest_framework import filters, permissions, status, viewsets
from rest_framework.response import Response

from api.serializers import ImageCreateSerializer, ImageSerializer

logger = logging.getLogger(__name__)

class ImageViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post')
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title',)

    @extend_schema(
        parameters=[
            # optional query params
            OpenApiParameter('width', OpenApiTypes.INT, OpenApiParameter.QUERY),
            OpenApiParameter('height', OpenApiTypes.INT, OpenApiParameter.QUERY),
        ],
        request=ImageCreateSerializer,
        responses=ImageSerializer,
    )
    def create(self, request, *args, **kwargs):
        serializer = ImageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        desired_width = request.query_params.get('width')
        desired_height = request.query_params.get('height')

        if not desired_height and not desired_width:
            # no resizing, save immediately
            img_obj = serializer.save()
            return Response(data=ImageSerializer(img_obj).data, status=status.HTTP_201_CREATED)

        real_width, real_height = serializer.validated_data['image'].image.size
        if not desired_height:
            desired_height = real_height
        if not desired_width:
            desired_width = real_width

        image_file = serializer.validated_data['image']
        image_file = Image.resize_image(image_file, desired_width, desired_height)
        serializer.validated_data['image'] = image_file
        img_obj = serializer.save()
        return Response(data=ImageSerializer(img_obj).data, status=status.HTTP_201_CREATED)
