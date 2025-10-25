from django.urls import path
from . import views

urlpatterns = [
    path("download/", views.download_extension, name="download_extension"),
]