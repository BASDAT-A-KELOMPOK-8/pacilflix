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

from daftar_favorit.views import delete_favorite, show_favorites

# from daftar_favorit.views import delete_favorite
from daftar_unduhan.views import show_downloads

from elements.views import elements_list
from langganan.views import show_subscription, show_checkout
from daftar_kontributor.views import show_contributors

from tayangan.views import tayangan_display, detail_tayangan

app_name = "authentication"
urlpatterns = [
    path("", show_main, name="show_main"),
    path("register/", register_page, name="register"),
    path("handle-register/", register, name="handle_register"),
    path("login/", login, name="login"),
    path("logout/", logout_user, name="logout"),
    path("favorites/", show_favorites, name="favorites"),
    path("favorites/delete/", delete_favorite, name="delete_favorite"),
    # path('<str:username>/favorites/delete/', delete_favorite, name='delete_favorite'),
    path("downloads/", show_downloads, name="downloads"),
    path("subscription/", show_subscription, name="subscription"),
    path("checkout/", show_checkout, name="checkout"),
    path("contributors/", show_contributors, name="contributors"),
    path("tayangan/", include("tayangan.urls"), name="tayangan"),
    # path("tayangan/detail_tayangan", detail_tayangan, name="detail_tayangan"),
]
