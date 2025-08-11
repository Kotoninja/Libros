from django.test import TestCase
from library.models import Book
from django.urls import reverse


class BookViewsTestHomePage(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        for i in range(20):
            book = Book.objects.create(
                title=f"Test{i}",
                description=f"Description{i}",
                price=100 * i,
            )
            book.add_tags(f"Tags{i}, Test{i}, Book{i}")

    def test_status_code(self):
        response = self.client.get(reverse("library:home"))
        self.assertEqual(response.status_code, 200)

    def test_html(self):
        response = self.client.get(reverse("library:home"))
        self.assertTemplateUsed(response, "library/home.html")

    def test_query_set(self):
        book_list = [i for i in Book.objects.all()]
        
        response = self.client.get(reverse("library:home") + "?page=1")
        self.assertEqual(list(response.context["page_obj"]), book_list[:12])
        
        response = self.client.get(reverse("library:home") + "?page=2")
        self.assertEqual(list(response.context["page_obj"]), book_list[12:])


class BookViewsTestCreateBookPage(TestCase):
    def test_create_book_form(self):
        response = self.client.get(reverse("library:create_book"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/create_book.html")

        response = self.client.post(
            reverse("library:create_book"),
            {"title": "Test", "description": "Description", "price": 100},
        )
        book = Book.objects.get(pk=1)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("library:book", args=(book.pk,)))

        response = self.client.get(reverse("library:book", args=(book.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/book.html")
        self.assertEqual(response.context["book"], Book.objects.get(pk=1))
        
