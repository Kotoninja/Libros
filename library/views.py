# Django
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.paginator import Paginator

# Other
from .models import Book
from .forms import CreateBookForm


def home(request):
    paginator = Paginator(Book.objects.all(),12)
    
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "library/home.html", {"page_obj": page_obj})


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
