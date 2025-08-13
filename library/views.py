# Django
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q

# Other
from .models import Book
from .forms import CreateBookForm
from core.forms import SearchForm


def home(request):
    paginator = Paginator(Book.objects.all(), 12)

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
    context: dict = {}

    if request.method == "GET":
        form = SearchForm(request.GET)
        if form.is_valid():
            search: str = form.cleaned_data["search"]

            books = Book.objects.filter(
                Q(title__contains=search)
                | Q(description__contains=search)
                | Q(tags__name__in=search.split())
            ).distinct()

            paginator = Paginator(books, 18)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            context |= {
                "page_obj": page_obj,
                "amount": books.count(),
                "search": search,
                "search_form": SearchForm(initial={"search": search}),
                "paginator": paginator,
            }
    else:
        form = SearchForm()

    return render(request, "library/search.html", context=context)
