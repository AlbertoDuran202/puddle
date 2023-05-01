from django.urls import path
from . import views
from .views import add_to_cart, remove_from_cart, view_cart, update_cart, checkout

app_name = 'item'

urlpatterns = [
    path("<int:pk>/", views.item_detail, name="detail"),
    path('add_to_cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:pk>/', remove_from_cart, name='remove_from_cart'),
    path('view_cart/', view_cart, name='view_cart'),
    path('update_cart/<int:pk>/', update_cart, name='update_cart'),
    path('checkout/', checkout, name='checkout'),
]
