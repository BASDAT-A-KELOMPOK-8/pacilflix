from django import forms

class SimpleUserCreationForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Nama Pengguna',
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label='Kata Sandi'
    )
    negara_asal = forms.CharField(
        max_length=100,
        required=True,
        label='Negara Asal'
    )
