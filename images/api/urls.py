from django.urls import path

from . import views

urlpatterns = [
    path('images/', views.ImageList.as_view(), name='image_list'),
    path('images/upload/', views.ImageUpload.as_view(), name='image_upload'),
    path('images/<int:id>/create_temp/', views.CreateTemporaryLink.as_view(), name='create_temporary_link'),
    path('images/temporary_links/', views.TemporaryLinksList.as_view(), name='temporary_links_list'),
]
