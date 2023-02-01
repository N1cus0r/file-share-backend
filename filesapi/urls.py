from django.urls import path
from .views import CreateSharedDataInstance, GetDataInstance


urlpatterns = [
    path("upload-data", CreateSharedDataInstance.as_view()),
    path("get-data-instance", GetDataInstance.as_view()),
]
