from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
# TODO expand user db, add username (create log in with login), location, phone number, birthday
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    nickname = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    photo = models.ImageField(
        upload_to="images/%Y/%m/%d",
        default=f"{settings.STATICFILES_DIRS}/images/default_user_photo.png",
    )
    birthday = models.DateField(blank=True, null=True)

    def __str__(self) -> str:
        if self.nickname:
            return self.nickname
        return "Nickname Default"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **Kwargs):
    if created:
        UserProfile.objects.create(user=instance, nickname=instance.username)
