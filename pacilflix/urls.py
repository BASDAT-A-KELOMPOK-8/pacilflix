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

from django.urls import include, path
from authentication.views import login, register, logout_user, register_page
from authentication.views import show_main

from daftar_favorit.views import show_favorites, show_favorite_details, add_favorite, delete_favorite, add_favorite_item, delete_favorited_item
from daftar_unduhan.views import add_download, delete_download, show_downloads

from langganan.views import show_subscription, show_checkout, add_transaction
from daftar_kontributor.views import show_contributors

from tayangan.views import detail_tayangan, tayangan_display

app_name = "authentication"
urlpatterns = [

    path("", show_main, name="show_main"),
    path("register/", register_page, name="register"),
    path("handle-register/", register, name="handle_register"),
    path("login/", login, name="login"),
    path("logout/", logout_user, name="logout"),

    path("subscription/", show_subscription, name="subscription"),
    path("checkout/", show_checkout, name="checkout"),
    path("contributors/", show_contributors, name="contributors"),

    path('favorites/', show_favorites, name='favorites'),
    path('favorites/<str:judul>/<str:timestamp>/<str:username>/', show_favorite_details, name='favorite_details'),
    path('add_favorite/<str:judul>', add_favorite, name='add_favorite'),
    path('addfavoriteitem/<uuid:id_tayangan>/<str:timestamp>', add_favorite_item, name='add_favorite_item'),
    path('delete/<str:judul>/<str:timestamp>/', delete_favorite, name='delete_favorite'),
    path('deleteitem/<uuid:id_tayangan>/<str:timestamp>/', delete_favorited_item, name='delete_favorited_item'),

    path('downloads/', show_downloads, name='downloads'),
    path('delete_download/<uuid:id_tayangan>/<str:timestamp>/', delete_download, name='delete_download'),
    path('add_download/<uuid:id_tayangan>/', add_download, name='add_download'),

    path('subscription/', show_subscription, name='subscription'),
    path('checkout/', show_checkout, name='checkout'),
    path('contributors/', show_contributors, name='contributors'),

    path("tayangan/", include("tayangan.urls")),
]
