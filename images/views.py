from datetime import timezone

from django.http import FileResponse, HttpResponse
from django.utils import timezone

from .models import TemporaryLink


def temporary_link_to_image(request, slug):
    temp_link = TemporaryLink.objects.get(slug=slug)
    if temp_link.expiration > timezone.now():
        response = FileResponse(open(temp_link.image.image.path, 'rb'))
        return response
    else:
        temp_link.delete()
        return HttpResponse(status=404)

