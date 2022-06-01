from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied, ValidationError

from ..models import *
from .serializers import *
from .permissions import HasTempLinkPermission


class ImageList(generics.ListAPIView):

    serializer_class = ImageSerializer

    def get_queryset(self):
        queryset = Image.objects.filter(user=self.request.user)
        return queryset


class ImageUpload(generics.CreateAPIView):

    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CreateTemporaryLink(generics.CreateAPIView):

    serializer_class = TemporaryLinkSerializer
    permission_classes = [HasTempLinkPermission]

    def perform_create(self, serializer):

        try:
            image = Image.objects.get(id=self.kwargs['id'])
            if image.user == self.request.user:
                serializer.save(image=image)
            else:
                raise PermissionDenied({'error': 'You can not access this image'})
        except ObjectDoesNotExist:
            raise ValidationError({'error': 'Image doesnt exist'})


class TemporaryLinksList(generics.ListAPIView):

    serializer_class = TemporaryLinkSerializer

    def get_queryset(self):
        queryset = TemporaryLink.objects.filter(image__user=self.request.user)
        return queryset

