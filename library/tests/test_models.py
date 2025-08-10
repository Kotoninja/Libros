from django.test import TestCase
from django.db.models import NOT_PROVIDED


from library.models import Book


class BookModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        b = Book.objects.create(title="Title", description="Description", price=100)
        b.add_tags("Test, Tags,Book")

    def test_title_label(self):
        book = Book.objects.get(pk=1)
        title_field = book._meta.get_field("title")
        self.assertEqual(title_field.verbose_name, "title")
        self.assertEqual(title_field.max_length, 50)
        self.assertEqual(title_field.default, NOT_PROVIDED)

    def test_rating_label(self):
        book = Book.objects.get(pk=1)
        title_field = book._meta.get_field("rating")
        self.assertEqual(title_field.verbose_name, "rating")
        self.assertEqual(title_field.default, 0)

    def test_description_label(self):
        book = Book.objects.get(pk=1)
        title_field = book._meta.get_field("description")
        self.assertEqual(title_field.verbose_name, "description")
        self.assertEqual(title_field.max_length, 2000)
        self.assertEqual(title_field.default, NOT_PROVIDED)

    def test_price_label(self):
        book = Book.objects.get(pk=1)
        title_field = book._meta.get_field("price")
        self.assertEqual(title_field.verbose_name, "price")
        self.assertEqual(title_field.max_length, None)
        self.assertEqual(title_field.default, NOT_PROVIDED)

    def test_feedbacks_label(self):
        book = Book.objects.get(pk=1)
        title_field = book._meta.get_field("feedbacks")
        self.assertEqual(title_field.verbose_name, "feedbacks")
        self.assertEqual(title_field.max_length, None)
        self.assertEqual(title_field.default, 0)

    def test_created_label(self):
        book = Book.objects.get(pk=1)
        title_field = book._meta.get_field("created")
        self.assertEqual(title_field.verbose_name, "created")
        self.assertEqual(title_field.auto_now_add, True)
        self.assertEqual(title_field.db_index, True)

    def test_image_label(self):
        book = Book.objects.get(pk=1)
        title_field = book._meta.get_field("image")
        self.assertEqual(title_field.verbose_name, "image")
        self.assertEqual(title_field.upload_to, "images/%Y/%m/%d")
        self.assertEqual(title_field.default, "images/default.webp")

    def test_book_str(self):
        book = Book.objects.get(pk=1)
        self.assertEqual(str(book), book.title)
        
    def test_book_get_absolute_url(self):
        book = Book.objects.get(pk=1)
        self.assertEqual(book.get_absolute_url(), "/book/1")

    def test_tags_str(self):
        book = Book.objects.get(pk=1)
        self.assertEqual(book.tags_str(), ", ".join(o.name for o in book.tags.all()))
