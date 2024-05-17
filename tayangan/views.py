from django.shortcuts import render
from django.db import connection
from models.tayangan import tayangan


# Create your views here.
def tayangan_display(request):
    return render(request, "tayangan.html")


def get_pengguna(self):
    with connection.cursor() as cursor:

        cursor.execute("SELECT * from pengguna")
        data = cursor.fetchall()
        print(tayangan.testing())

    return data


def tayangan_detail(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * from film")
        data_tayangan = cursor.fetchall()
        print(data_tayangan)

    return render(data_tayangan, "detail_tayangan.html")


def detail_series(request):
    return render(request, "detail_series.html")


def detail_episode(request):
    return render(request, "detail_episode.html")


def daftar_trailer(request):
    return render(request, "trailer.html")
