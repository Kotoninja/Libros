from django.urls import path

from . import views

app_name = "library"

urlpatterns = [
    path("", views.home, name="home"),
    path("create_book/", views.create_book, name="create_book"),
    path("book/<int:id>", views.book, name="book"),
    path("search/", views.search, name="search"),
    path("random/",views.get_random_book,name="random")
]
