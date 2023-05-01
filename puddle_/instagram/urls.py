from django.urls import path
from . import views

urlpatterns = [
  path('instagram/', views.get_instagram_feed, name='instagram_images')
]