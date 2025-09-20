from django.shortcuts import render, redirect, get_object_or_404
from library.models import Book
from django.views.decorators.http import require_POST
from django.urls import reverse
from .cart import Cart
from django.http import HttpResponse
from django.template.loader import render_to_string

"""
TODO add a counter to the cart
TODO increase/reduce cart counter when add book
"""


@require_POST
def cart_add(request, book_id):
    print("add product to cart")
    cart = Cart(request)
    product = get_object_or_404(Book, id=book_id)
    cart.add(product=product, quantity=1, update_quantity=True)
    return HttpResponse(render_to_string(request=request, template_name="library/remove_book_from_cart.html",context={"book":product}))



@require_POST
def cart_remove(request, book_id):
    cart = Cart(request)
    product = get_object_or_404(Book, id=book_id)
    cart.remove(product)

    return HttpResponse(render_to_string(request=request, template_name="library/add_book_to_cart.html",context={"book":product}))



def remove_all(request):
    cart = Cart(request)
    cart.clear()
    return redirect(reverse("library:home"))
