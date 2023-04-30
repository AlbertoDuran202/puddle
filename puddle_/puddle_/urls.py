from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from core.views import index, contact
from instagram import views as instagram_views

urlpatterns = [
    path("", index, name="index"),
    path("contact/", contact, name="contact"),
    path("item/", include("item.urls")),
    path("admin/", admin.site.urls),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", include("core.urls", namespace="core")), 
    path('instagram/', include('instagram.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
