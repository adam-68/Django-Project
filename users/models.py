from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
import datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100,  default='')
    email = models.EmailField(max_length=150, default='')
    birth_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("user_profile", args=[self.user.username])


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()