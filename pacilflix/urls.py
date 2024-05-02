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

from authentication.views import register 
from authentication.views import login_user, logout_user
from authentication.views import show_main

from daftar_favorit.views import show_favorites
# from daftar_unduhan import 

app_name = 'authentication'
urlpatterns = [
    path('', show_main, name='show_main'),
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'), 
    path('logout/', logout_user, name='logout'),

    path('favorites/', show_favorites, name='favorites'),
]
