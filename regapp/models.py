from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    email_confirmed = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, null=True)
    location = models.CharField(max_length=30, null=True)
    birth_date = models.DateField(null=True)

    def __str__(self):
      return self.user.username




def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = Profile(user=user)
        user_profile.save()
post_save.connect(create_profile, sender=User)

