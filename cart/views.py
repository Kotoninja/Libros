from django.shortcuts import render, redirect, get_object_or_404
from library.models import Book
from django.views.decorators.http import require_POST
from django.urls import reverse
from .cart import Cart
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.cache import cache
import json

"""
TODO: Add ajax check
"""


def validation_cache(request):
    print("cart_validation update")
    cache.delete(f"user_cart_{request.user.id}")


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Book, id=product_id)
    cart.add(product=product, quantity=1, update_quantity=True)
    validation_cache(request=request)

    response = HttpResponse(
        render_to_string(
            request=request,
            template_name="library/remove_book_from_cart.html",
            context={"book": product},
        )
    )
    response["Hx-Trigger"] = "cartCounterUpdate"
    return response


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Book, id=product_id)
    cart.remove(product)
    validation_cache(request=request)

    response = HttpResponse(
        render_to_string(
            request=request,
            template_name="library/add_book_to_cart.html",
            context={"book": product},
        )
    )
    response["Hx-Trigger"] = "cartCounterUpdate"
    return response


def get_lenght_items(request):
    cart = Cart(request)
    return HttpResponse(len(cart), status=200)


@require_POST
def update_quantity(request, product_id, quantity):
    if quantity > 0:
        cart = Cart(request)
        product = get_object_or_404(Book, id=product_id)
        cart.add(product=product, quantity=quantity, update_quantity=True)
        validation_cache(request=request)

        quantity, price = cart.get_item(product_id=product_id).values()

        item = {
            "product": product,
            "quantity": quantity,
            "price": price,
            "total_price": (int(quantity) * int(price)),
        }
        response = render(request, "cart/cart_item.html", context={"item": item})
        response["Hx-Trigger"] = "cartCounterUpdate,cartPriceUpdate"

        return response

    return HttpResponse(status="204")


def get_total_price(request):
    cart = Cart(request)
    return HttpResponse(cart.get_total_price())


def delete(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Book, id=product_id)
    cart.remove(product)
    validation_cache(request=request)

    response = HttpResponse("")
    response["Hx-Trigger"] = "cartCounterUpdate,cartPriceUpdate"
    return response
