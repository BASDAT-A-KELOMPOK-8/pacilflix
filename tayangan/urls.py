from django.urls import path
from tayangan.views import *
from . import views

app_name = "tayangan"

urlpatterns = [
    path("", views.tayangan_display, name="dashboard"),
    path("search_tayangan/", views.search, name="search_tayangan"),
    path("trailer", views.trailer_display, name="trailer"),
    path("detail_tayangan/<uuid:id>", views.detail_tayangan, name="detail_tayangan"),
    path("submit_slider/<uuid:id>", views.submit_slider, name="submit_slider"),
    path("submit_ulasan/<uuid:id>", views.submit_ulasan, name="submit_ulasan"),
    path(
        "detail_tayangan/submit_ulasan/<str:id>",
        views.submit_ulasan,
        name="submit_ulasan",
    ),
]
