from django.shortcuts import render

def show_contributors(request):
    context = {}
    return render(request, "contributors.html", context)
