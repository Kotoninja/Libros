from django.shortcuts import render, redirect, get_object_or_404
from library.models import Book
from django.views.decorators.http import require_POST
from django.urls import reverse
from .cart import Cart
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib import messages
import json


"""
TODO Add ajax check
"""


@require_POST
def cart_add(request, book_id):
    cart = Cart(request)
    product = get_object_or_404(Book, id=book_id)
    cart.add(product=product, quantity=1, update_quantity=True)
    response = HttpResponse(
        render_to_string(
            request=request,
            template_name="library/remove_book_from_cart.html",
            context={"book": product},
        )
    )
    response["Hx-Trigger"] = "cartUpdated"
    return response


@require_POST
def cart_remove(request, book_id):
    cart = Cart(request)
    product = get_object_or_404(Book, id=book_id)
    cart.remove(product)

    response = HttpResponse(
        render_to_string(
            request=request,
            template_name="library/add_book_to_cart.html",
            context={"book": product},
        )
    )
    response["Hx-Trigger"] = "cartUpdated"
    return response


def get_lenght_items(request):
    cart = Cart(request)
    cart_lenght = len(cart)
    if cart_lenght:
        return HttpResponse(len(cart), status=200)
    return HttpResponse()
