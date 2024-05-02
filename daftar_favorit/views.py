from django.shortcuts import render

def show_favorites(request):
    context = {}
    return render(request, "favorites.html", context)
