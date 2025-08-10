# Django
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

# Other
from .models import Book
from .forms import CreateBookForm


def home(request):
    context = {"books": Book.objects.all()}
    return render(request, "library/home.html", context=context)


def book(request, id):
    book = get_object_or_404(Book, pk=id)
    return render(request, "library/book.html", context={"book": book})


def create_book(request):
    if request.method == "POST":
        form = CreateBookForm(request.POST, request.FILES)

        if form.is_valid():
            new_book = form.save()
            return HttpResponseRedirect(reverse("library:book", args=(new_book.pk,)))

    else:
        form = CreateBookForm()

    return render(request, "library/create_book.html", context={"form": form})


def search(request):
    pass
