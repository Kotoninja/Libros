from django.core.management.base import BaseCommand, CommandError
from library.models import Book


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.allow_abbrev = False
        parser.add_argument("add", type=int, nargs="+")

    def handle(self, *args, **options):
        for i in range(options["add"][0]):
            book = Book.objects.create(
                title=f"Test{i}",
                description=f"Description{i}",
                price=100 * i,
            )
            book.add_tags(f"Tags{i}, Test{i}, Book{i}")

        self.stdout.write(self.style.SUCCESS(f"Successfully created {options['add']} books"))
