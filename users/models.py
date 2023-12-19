from django.db import models
from django.contrib.auth.models import AbstractUser

GENDER_SELECTION = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('NS', 'Not Specified'),
)

class CustomUser(AbstractUser):
    gender = models.CharField(max_length=2, choices=GENDER_SELECTION)
    profile_photo = models.ImageField(
        upload_to="profile_images/", blank=True
    )