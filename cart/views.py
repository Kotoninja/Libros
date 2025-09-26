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
TODO add a counter to the cart
TODO increase/reduce cart counter when add book
TODO add alert when add/remove book in/from cart
"""


@require_POST
def cart_add(request, book_id):
    print("add product to cart")
    cart = Cart(request)
    product = get_object_or_404(Book, id=book_id)
    cart.add(product=product, quantity=1, update_quantity=True)
    # return HttpResponse(
    #     status=204,
    #     headers={"HX-Trigger": json.dumps({"messages": [{"messages": message.message, "tags": message.tags}for message in messages.get_messages(request)]})})
    # render_to_string(request=request, template_name="library/remove_book_from_cart.html",context={"book":product})
    # return HttpResponse(render_to_string(request=request, template_name="library/remove_book_from_cart.html",context={"book":product}), headers = {"HX-Trigger": json.dumps({"messages": [{"messages": message.message, "tags": message.tags}for message in messages.get_messages(request)]})})
    return HttpResponse(headers={"HX-Trigger":json.dumps({"Hello":"Hello"} )})

@require_POST
def cart_remove(request, book_id):
    cart = Cart(request)
    product = get_object_or_404(Book, id=book_id)
    cart.remove(product)

    return HttpResponse(
        render_to_string(
            request=request,
            template_name="library/add_book_to_cart.html",
            context={"book": product},
        )
    )


def remove_all(request):
    cart = Cart(request)
    cart.clear()
    return redirect(reverse("library:home"))
