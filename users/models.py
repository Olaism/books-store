from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    profile_photo = models.ImageField(
        upload_to="profile_images/", blank=True
    )