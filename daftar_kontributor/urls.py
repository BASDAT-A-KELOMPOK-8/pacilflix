from django.urls import path
from .views import contributors_view

urlpatterns = [
    path('contributors/', views.contributors_view, name='contributors'),
]