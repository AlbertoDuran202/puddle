from django.urls import path, include
from . import views
from .views import CustomLoginView


app_name = 'core'

urlpatterns = [
    # ... otras rutas URL ...
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
   

    
]