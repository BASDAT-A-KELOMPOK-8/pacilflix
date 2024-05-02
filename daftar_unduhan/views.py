from django.shortcuts import render

def show_downloads(request):
    context = {}
    return render(request, "downloads.html", context)
