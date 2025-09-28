from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("add/<book_id>", views.cart_add, name="add"),
    path("remove/<book_id>",views.cart_remove,name="remove"),
    path("len/",views.get_lenght_items,name="len"),
    path("get_total_price/",views.get_total_price,name="get_total_price"),
    path("update_quantity/<str:product_id>/<int:quantity>",views.update_quantity,name="update_quantity"),
]