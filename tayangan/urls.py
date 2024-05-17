from django.urls import path
from . import views

urlpatterns = [
    path("get_pengguna", views.get_pengguna, name="get-pengguna"),
]
