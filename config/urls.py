from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("drf_social_oauth2.urls", namespace="drf")),
    path("users/", include("users.urls")),
    path("files/", include("filesapi.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
