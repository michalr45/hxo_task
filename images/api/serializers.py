from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

from ..models import Image, TemporaryLink


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('id', 'image', 'thumbnails')

    thumbnails = serializers.SerializerMethodField()
    image = serializers.ImageField(validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])])

    def get_thumbnails(self, obj):
        user = self.context['request'].user
        request = self.context.get('request')

        thumbnails = []
        for size in user.subscription.thumbnail_heights:
            thumbnails.append(
                f"{size}px: {request.build_absolute_uri(get_thumbnail(obj.image, f'x{size}', crop='center', quality=99).url)}"
            )
        return thumbnails

    def __init__(self, *args, **kwargs):

        # Don't return the link to original file if user's subscription doesn't contain this feature
        original_link_perm = kwargs['context']['request'].user.subscription.link_to_original_file
        if original_link_perm is False:
            self.fields['image'].write_only = True

        super().__init__(*args, **kwargs)


class TemporaryLinkSerializer(serializers.ModelSerializer):

    class Meta:
        model = TemporaryLink
        fields = ('duration', 'expiration', 'temporary_link')

    expiration = serializers.CharField(read_only=True)
    temporary_link = serializers.SerializerMethodField()

    def get_temporary_link(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.get_absolute_url())
