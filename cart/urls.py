from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("add/<book_id>", views.cart_add, name="add"),
]
