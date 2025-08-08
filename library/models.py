from django.db import models
from taggit.managers import TaggableManager
from django.urls import reverse


class Book(models.Model):
    author = models.CharField(default="Anon")
    title = models.CharField(max_length=50)
    rating = models.FloatField(default=0)
    description = models.CharField(max_length=200, blank=True, null=True)
    price = models.PositiveIntegerField(default=0)
    feedbacks = models.PositiveIntegerField(default=0)
    tags = TaggableManager()
    created = models.DateField(auto_now_add=True, db_index=True)
    image = models.ImageField(
        upload_to="images/%Y/%m/%d", default="images/default.webp"
    )

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("library:book", kwargs={"pk": self.pk})

    def tags_str(self) -> str:
        return ", ".join(o.name for o in self.tags.all())

    def add_tags(self, tags):
        for tag in tags.split(","):
            self.tags.add(tag.strip())
