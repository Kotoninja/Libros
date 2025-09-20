from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("add/<book_id>", views.cart_add, name="add"),
    path("remove_all/", views.remove_all, name="remove_all"),
    path("remove/<book_id>",views.cart_remove,name="remove")
]
