from django.urls import path
from tayangan.views import *

urlpatterns = [
    path('tayangan', tayangan_display, name='tayangan'),
    path('detail_tayangan', tayangan_detail, name='detail_tayangan'),
    path('detail_series', detail_series, name='detail_series'),
    path('detail_episode', detail_episode, name='detail_episode'),
    path('daftar_trailer', daftar_trailer, name='daftar_trailer'),
]