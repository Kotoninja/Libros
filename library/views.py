# Django
from django.shortcuts import render

# Other
from .models import Book


def home(request):
    context = {"books": Book.objects.all()}
    return render(request, "library/home.html", context=context)


def book(request):
    pass


def create_book(request):
    return render(request, "library/create_book.html")


def search(request):
    pass
