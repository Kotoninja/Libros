from django.shortcuts import render, redirect, get_object_or_404
from library.models import Book
from django.views.decorators.http import require_POST
from .cart import Cart


@require_POST
def cart_add(request, book_id):
    print("add product to cart")
    cart = Cart(request)
    product = get_object_or_404(Book, id=book_id)
    cart.add(product=product, quantity=1, update_quantity=True)
