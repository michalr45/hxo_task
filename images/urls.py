from django.urls import path

from . import views

urlpatterns = [
    path('temp_url/<slug:slug>/', views.temporary_link_to_image, name='temp_link')
]
