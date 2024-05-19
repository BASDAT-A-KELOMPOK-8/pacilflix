"""
URL configuration for pacilflix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from authentication.views import login, register, logout_user, register_page
from authentication.views import show_main

from daftar_favorit.views import show_favorites, show_favorite_details, add_favorite, delete_favorite, add_favorite_item, delete_favorited_item
from daftar_unduhan.views import show_downloads

from elements.views import elements_list
from langganan.views import show_subscription, show_checkout
from daftar_kontributor.views import show_contributors

from tayangan.views import tayangan_display, tayangan_detail, detail_series, detail_episode, daftar_trailer

app_name = 'authentication'
urlpatterns = [
    path('', show_main, name='show_main'),
    path('admin/', admin.site.urls),
    path('register/', register_page, name='register'),
    path('handle-register/', register, name='handle_register'),
    path('login/', login, name='login'), 
    path('logout/', logout_user, name='logout'),

    path('favorites/', show_favorites, name='favorites'),
    path('favorites/<str:judul>/<str:timestamp>/<str:username>/', show_favorite_details, name='favorite_details'),
    path('add_favorite/<str:judul>', add_favorite, name='add_favorite'),
    # path('addfavoriteitem/<str:judul>', add_favorite_item, name='add_favorite_item'),
    path('delete/<str:judul>/<str:timestamp>/', delete_favorite, name='delete_favorite'),
    path('deleteitem/<uuid:id_tayangan>/<str:timestamp>/', delete_favorited_item, name='delete_favorited_item'),

    path('downloads/', show_downloads, name='downloads'),

    path('subscription/', show_subscription, name='subscription'),
    path('checkout/', show_checkout, name='checkout'),
    path('contributors/', show_contributors, name='contributors'),

    path('tayangan/', tayangan_display, name='tayangan'),
    path('tayangan/detail/', tayangan_detail, name='tayangan_detail'),
    path('tayangan/detail/series/', detail_series, name='detail_series'),
    path('tayangan/detail/episode/', detail_episode, name='detail_episode'),
    path('tayangan/trailer/', daftar_trailer, name='daftar_trailer'),
]
