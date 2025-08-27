# Django
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages

# Other
from .models import Book
from .forms import CreateBookForm, AdditionalSearchFilter
from core.forms import SearchForm


def get_errors_from_form(request, form):
    for error_field, error_message in form.errors.as_data().items():
        messages.error(
            request,
            f"{error_field.capitalize().replace('_', ' ')} : {error_message[0].message}",
        )


def home(request):
    paginator = Paginator(Book.objects.all(), 12)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "library/home.html", {"page_obj": page_obj})


def book(request, id):
    def get_rating(rating) -> list:
        rating_list: list = []
        rating = rating
        i = 5
        while i != 0:
            if rating > 0:
                if rating >= 1:
                    rating_list.append(1)
                else:
                    rating_list.append(0.5)
            else:
                rating_list.append(0)
            rating -= 1
            i -= 1
        return rating_list

    book = get_object_or_404(Book, pk=id)
    return render(
        request,
        "library/book.html",
        context={"book": book, "rating": get_rating(book.rating)},
    )


def create_book(request):
    if request.method == "POST":
        form = CreateBookForm(request.POST, request.FILES)

        if form.is_valid():
            new_book = form.save()
            return HttpResponseRedirect(reverse("library:book", args=(new_book.pk,)))

    else:
        form = CreateBookForm()

    return render(
        request,
        "library/create_book.html",
        context={"form": form, "errors": form.errors},
    )


def search(request):
    context: dict = {"filter_form": AdditionalSearchFilter()}

    books = Book.objects.all()

    search_form = SearchForm(request.GET or None)
    filter_form = AdditionalSearchFilter(request.GET or None)

    if search_form.is_valid() and search_form.cleaned_data["search"]:
        search: str = search_form.cleaned_data["search"]
        context |= {"search": search}

        books = books.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(tags__name__in=search.split())
        ).distinct()

    if filter_form.is_valid():
        if filter_form.cleaned_data.get("is_rating_upper"):
            books = books.filter(rating__gte=4.7)

        price_from: int | None = filter_form.cleaned_data.get("price_from")
        price_to: int | None = filter_form.cleaned_data.get("price_to")

        if price_from and price_to:
            if price_from > price_to:
                books = books.filter(price__gte=price_from, price__lte=price_from * 1.5)
            else:
                books = books.filter(price__gte=price_from, price__lte=price_to)

        else:
            if filter_form.cleaned_data.get("price_from"):
                books = books.filter(price__gte=filter_form.cleaned_data["price_from"])

            if filter_form.cleaned_data.get("price_to"):
                books = books.filter(price__lte=filter_form.cleaned_data["price_to"])

    paginator = Paginator(books, 30)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context |= {
        "amount": books.count(),
        "search_form": search_form,
        "filter_form": filter_form,
        "page_obj": page_obj,
        "paginator": paginator,
        "errors": get_errors_from_form(request, form=filter_form),
    }

    return render(request, "library/search.html", context=context)
