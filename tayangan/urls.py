from django.urls import path
from . import views

app_name = "tayangan"
urlpatterns = [
    path("", views.tayangan_display, name="dashboard"),
    path("detail_tayangan/", views.detail_tayangan, name="detail_tayangan"),
]
