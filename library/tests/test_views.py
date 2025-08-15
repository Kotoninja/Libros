from django.test import TestCase
from library.models import Book
from django.urls import reverse
from faker import Faker
from random import uniform


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


class BookViewTestSearch(TestCase):
    TITLE = "Kotoninja"
    DESCRIPTION = "Artem"
    TAG1 = "Lox"
    TAG2 = "Jopa"
    TAG3 = "debil"

    @classmethod
    def setUpTestData(cls) -> None:
        fake = Faker()
        for i in range(25):
            book = Book.objects.create(
                title=fake.text(max_nb_chars=20),
                description=fake.paragraph(),
                price=100 * i,
            )
            book.add_tags(", ".join(fake.words()))

        for j in range(25):
            book = Book.objects.create(
                title=f"{cls.TITLE}{j}",
                description=f"{cls.DESCRIPTION}{j}",
                price=100 * j,
            )
            book.add_tags(f"{cls.TAG1}{j}, {cls.TAG2}{j}, {cls.TAG3}{j}")

    def test_send_search_request(self):
        books_list: list = []
        page: int = 1
        exepted_page: None | int = None
        while page <= (exepted_page if exepted_page else 1):
            response = self.client.get(
                reverse("library:search"), {"search": self.TITLE, "page": page}
            )

            self.assertTemplateUsed(response, "library/search.html")

            if exepted_page is None:
                exepted_page = response.context["paginator"].num_pages

            for book in response.context["page_obj"]:
                books_list.append(book)

            page += 1

        self.assertEqual(
            list(Book.objects.filter(title__contains=self.TITLE)), books_list
        )

    def test_send_search_request_all_field(self):
        books = Book.objects.filter(
            title__contains=self.TITLE,
            description__contains=self.DESCRIPTION,
        )

        response = self.client.get(reverse("library:search"), {"search": self.TITLE})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/search.html")
        self.assertQuerySetEqual(response.context["paginator"].object_list, books)

        response = self.client.get(
            reverse("library:search"), {"search": self.DESCRIPTION}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "library/search.html")
        self.assertQuerySetEqual(response.context["paginator"].object_list, books)


class BookViewsTestAdditionalSearchFilter(TestCase):
    TITLE = "Kotoninja"
    DESCRIPTION = "Artem"
    TAG1 = "Lox"
    TAG2 = "Jopa"
    TAG3 = "debil"
    PRICE_FROM_TO = 1300

    @classmethod
    def setUpTestData(cls) -> None:
        fake = Faker()
        for i in range(25):
            book = Book.objects.create(
                title=fake.text(max_nb_chars=20),
                description=fake.paragraph(),
                price=100 * i,
                rating=float(f"{uniform(1, 4.6):.1f}"),
            )
            book.add_tags(", ".join(fake.words()))

        for j in range(25):
            book = Book.objects.create(
                title=f"{cls.TITLE}{j}",
                description=f"{cls.DESCRIPTION}{j}",
                price=100 * j,
                rating=4.8,
            )
            book.add_tags(f"{cls.TAG1}{j}, {cls.TAG2}{j}, {cls.TAG3}{j}")

    def test_apply_is_ratting_upper(self):
        books = Book.objects.filter(rating__gte=4.7)
        response = self.client.get(
            reverse("library:search"), {"search": self.TITLE, "is_rating_upper": "on"}
        )
        self.assertTemplateUsed(response, "library/search.html")
        self.assertQuerySetEqual(response.context["paginator"].object_list, books)

    def test_apply_price_from(self):
        books = Book.objects.filter(
            price__gte=self.PRICE_FROM_TO, title__icontains=self.TITLE
        )
        response = self.client.get(
            reverse("library:search"),
            {"search": self.TITLE, "price_from": str(self.PRICE_FROM_TO)},
        )
        self.assertTemplateUsed(response, "library/search.html")
        self.assertQuerySetEqual(response.context["paginator"].object_list, books)

    def test_apply_price_to(self):
        books = Book.objects.filter(
            price__lte=self.PRICE_FROM_TO, title__icontains=self.TITLE
        )
        response = self.client.get(
            reverse("library:search"),
            {"search": self.TITLE, "price_to": str(self.PRICE_FROM_TO)},
        )
        self.assertTemplateUsed(response, "library/search.html")
        self.assertQuerySetEqual(response.context["paginator"].object_list, books)

    def test_price_from_greater_price_to(self):
        response = self.client.get(
            reverse("library:search"),
            {
                "search": self.TITLE,
                "price_from": str(self.PRICE_FROM_TO + 10),
                "price_to": str(self.PRICE_FROM_TO - 10),
            },
        )
        self.assertTrue(response.context["paginator"].object_list)

    def test_additional_filter_with_pagination(self):
        books = list(
            Book.objects.filter(
                title__icontains=self.TITLE,
                rating__gte=4.7,
                price__gte=100,
                price__lte=2000,
            )
        )
        response = self.client.get(
            reverse("library:search"),
            {
                "search": self.TITLE,
                "is_rating_upper": "on",
                "price_from": str(100),
                "price_to": str(2000),
            },
        )
        p = response.context["paginator"]

        total_pagination_book: list = []
        for i in range(1, p.num_pages + 1):
            total_pagination_book.extend(p.page(i).object_list)
        self.assertEqual(total_pagination_book, books)
