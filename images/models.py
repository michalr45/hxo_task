import os
import uuid
from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import (FileExtensionValidator, MaxValueValidator,
                                    MinValueValidator)
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django_better_admin_arrayfield.models.fields import ArrayField


def user_images_path(instance, filename):
    return f'images/{instance.user.username}/{str(uuid.uuid4())}/{filename}'


class Subscription(models.Model):
    name = models.CharField(max_length=60)
    thumbnail_heights = ArrayField(models.PositiveIntegerField())
    link_to_original_file = models.BooleanField(default=False)
    generate_expiring_links = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class User(AbstractUser):
    subscription = models.OneToOneField(Subscription,
                                        related_name='subscription',
                                        on_delete=models.SET_NULL,
                                        null=True)


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='images',
                             on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_images_path,
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])])

    def __str__(self):
        return f'{self.user.username}_{os.path.basename(self.image.name)}'


class TemporaryLink(models.Model):
    image = models.ForeignKey(Image,
                              related_name='temporary_links',
                              on_delete=models.CASCADE)
    duration = models.PositiveIntegerField(default=300,
                                           validators=[
                                               MinValueValidator(300),
                                               MaxValueValidator(30000)
                                           ])
    expiration = models.DateTimeField()
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.expiration = timezone.now() + timedelta(seconds=self.duration)
        self.slug = slugify('temp_' + str(uuid.uuid4()))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('temp_link', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.image.user.username}_{os.path.basename(self.image.image.name)}_{str(self.expiration)}'
