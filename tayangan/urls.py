from django.urls import path
from . import views

app_name = "tayangan"
urlpatterns = [
    path("", views.tayangan_display, name="dashboard"),
    path("detail_tayangan/<uuid:id>", views.detail_tayangan, name="detail_tayangan"),
    path(
        "detail_tayangan/submit_ulasan/<str:id>",
        views.submit_ulasan,
        name="submit_ulasan",
    ),
]
