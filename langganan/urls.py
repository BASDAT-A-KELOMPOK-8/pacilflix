from django.urls import path
from langganan.views import show_checkout

app_name = 'bookmark'

urlpatterns = [
    path('checkout/<str:package_name>/', show_checkout, name='checkout'),
]