from django.shortcuts import render

# Create your views here.
def tayangan_display(request):
    return render(request, "tayangan.html")

def tayangan_detail(request):
    return render(request, "detail_tayangan.html")

def detail_series(request):
    return render(request, "detail_series.html")

def detail_episode(request):
    return render(request, "detail_episode.html")

def daftar_trailer(request):
    return render(request, "trailer.html")