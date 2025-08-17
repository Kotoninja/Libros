from django.core.management.base import BaseCommand, CommandError
from library.models import Book
from faker import Faker
from random import uniform


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.allow_abbrev = False
        parser.add_argument("add", type=int, nargs="+")

    def handle(self, *args, **options):
        fake = Faker()
        for i in range(options["add"][0]):
            book = Book.objects.create(
                title=fake.text(max_nb_chars=20),
                description=fake.paragraph(),
                price=100 * i,
                rating=float(f"{uniform(1, 5):.1f}"),
            )
            book.add_tags(", ".join(fake.words()))

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {options['add']} books")
        )
