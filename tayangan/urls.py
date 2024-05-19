from django.urls import path
from tayangan.views import *
from . import views

urlpatterns = [
<<<<<<< HEAD
    path("tayangan", tayangan_display, name="tayangan"),
    path("detail_tayangan", tayangan_detail, name="detail_tayangan"),
    path("detail_series", detail_series, name="detail_series"),
    path("detail_episode", detail_episode, name="detail_episode"),
    path("daftar_trailer", daftar_trailer, name="daftar_trailer"),
    path("get_pengguna", views.get_pengguna, name="get-pengguna"),
]
=======
    path("", views.tayangan_display, name="dashboard"),
    path("detail_tayangan/<uuid:id>", views.detail_tayangan, name="detail_tayangan"),
    path("submit_slider/<uuid:id>", views.submit_slider, name="submit_slider"),
    path("submit_ulasan/<uuid:id>", views.submit_ulasan, name="submit_ulasan"),
    path(
        "detail_tayangan/submit_ulasan/<str:id>",
        views.submit_ulasan,
        name="submit_ulasan",
    ),
]
>>>>>>> e24baced8c69b39b16f8ad1301e9fa990a52ff98
