import io
import shutil
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image as PilImage
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Image, Subscription

User = get_user_model()
BASE_DIR = Path(__file__).resolve().parent.parent.parent


class LoginTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_1')
        self.user.set_password('testpassword123')

    def test_login(self):
        response = self.client.post('/api/auth/login/', data={
            'username': self.user.username,
            'password': self.user.password
        }, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class EndpointsTestCase(APITestCase):

    def generate_photo_file(self):
        bts = io.BytesIO()
        img = PilImage.new("RGB", (100, 100))
        img.save(bts, 'jpeg')
        return SimpleUploadedFile("test.jpg", bts.getvalue())

    def setUp(self):
        try:
            shutil.rmtree(f'{BASE_DIR}/media/tests', ignore_errors=True)
        except OSError:
            pass
        Image.image.field.storage.location = settings.TEST_ROOT
        self.user = User.objects.create_user(username='test_1',
                                             password='testpassword123')
        self.subscription = Subscription.objects.create(
            name='Sub',
            thumbnail_heights=[200, 400],
            link_to_original_file=True,
            generate_expiring_links=True
        )
        self.user.subscription = self.subscription
        self.client.force_authenticate(user=self.user)
        self.img = self.generate_photo_file()

    # GET

    def test_image_list_authenticated(self):
        response = self.client.get('/api/images/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_image_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/images/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_temp_links_list_authenticated(self):
        response = self.client.get('/api/images/temporary_links/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_temp_links_list_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/images/temporary_links/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # POST

    def test_create_temp_link(self):
        image = Image.objects.create(
            user=self.user,
            image=self.img
        )
        data = {
            'image': image,
            'duration': 300,
                }
        response = self.client.post(f'/api/images/{image.id}/create_temp/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_image(self):
        data = {
            'image': self.img
                }
        response = self.client.post('/api/images/upload/', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_image_unauthenticated(self):
        data = {
            'image': self.img
                }
        self.client.force_authenticate(user=None)
        response = self.client.post('/api/images/upload/', data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_temp_link_not_owner(self):
        image = Image.objects.create(
            user=self.user,
            image=self.img
        )
        self.client.force_authenticate(user=None)
        self.user_2 = User.objects.create_user(username='test_2',
                                               password='testpassword123')
        self.user_2.subscription = self.subscription
        self.client.force_authenticate(user=self.user_2)

        data = {
            'image': image,
            'duration': 300,
                }
        response = self.client.post(f'/api/images/{image.id}/create_temp/', data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_temp_link_non_existing_image(self):
        image = Image.objects.create(
            user=self.user,
            image=self.img
        )
        data = {
            'image': image,
            'duration': 300,
                }
        response = self.client.post(f'/api/images/{image.id}000/create_temp/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_temp_exp_validation(self):
        image = Image.objects.create(
            user=self.user,
            image=self.img
        )
        data = {
            'image': image,
            'duration': 299,
                }
        response = self.client.post(f'/api/images/{image.id}/create_temp/', data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)






