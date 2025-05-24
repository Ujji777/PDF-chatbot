from django.urls import path
from .views import UploadDocumentAPIView, QueryDocumentAPIView


urlpatterns = [
    path('upload/', UploadDocumentAPIView.as_view(), name='upload-document'),
    path("query/", QueryDocumentAPIView.as_view(), name="query-document"),
]
