# Django
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Other
from .models import *
from .forms import *


def home(request):
    context = {"books": Book.objects.all()}
    return render(request, "library/home.html", context=context)


def book(request):
    pass


def create_book(request):
    if request.method == "POST":
        form = CreateBookForm(request.POST, request.FILES)

        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return HttpResponseRedirect(reverse("library:home"))

    else:
        form = CreateBookForm()

    return render(request, "library/create_book.html", context={"form": form})

def search(request):
    pass
