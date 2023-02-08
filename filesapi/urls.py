from django.urls import path
from .views import CreateSharedDataInstance, GetDataInstance


app_name = 'files'


urlpatterns = [
    path("upload-data", CreateSharedDataInstance.as_view(), name='upload-data'),
    path("get-data-instance", GetDataInstance.as_view(), name='get-data-instance'),
]
