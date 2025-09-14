from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from .models import Book
from django.core.cache import cache


@receiver([post_save, post_delete], sender=Book)
def invalidate_books_chache_in_home_page(sender, instance, **kwargs):
    cache.delete_pattern("*home_page*")


@receiver([post_save, post_delete], sender=Book)
def invalidate_books_instance_cache(sender, instance, **kwargs):
    cache.delete_pattern(f"*book_page_{instance.pk}*")