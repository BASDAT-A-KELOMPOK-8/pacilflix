from django.shortcuts import render

def show_subscription(request):
    context = {}
    return render(request, "subscription.html", context)

def show_checkout(request):
    context = {}
    return render(request, "checkout.html", context)