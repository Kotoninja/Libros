from django.shortcuts import render


def home(request):
    context = {}
    return render(request, "library/home.html", context=context)
