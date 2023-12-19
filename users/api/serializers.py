from django.db import transaction
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

from ..models import GENDER_SELECTION

class CustomRegisterSerializer(RegisterSerializer):
    gender = serializers.ChoiceField(choices=GENDER_SELECTION)
    profile_photo = serializers.ImageField(max_length=150, allow_empty_file=True)

    # Define transaction.atomic to rollback the save operation in case of error
    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.profile_photo = self.data.get('profile_photo')
        user.gender = self.data.get('gender')
        user.save()
        return user