from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Formulir kustom yang memperluas UserCreationForm dengan field tambahan
class CustomUserCreationForm(UserCreationForm):
    negara_asal = forms.CharField(
        max_length=100, 
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'negara_asal')  # Tambahkan field baru ke daftar field
