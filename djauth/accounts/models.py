from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from django.db import models
from django.utils.text import slugify
from PIL import Image
import os
from django.conf import settings


class CustomUser(AbstractUser):
    username = None

    phone_number = models.CharField(max_length=12, unique=True)
    profile_image = models.ImageField(upload_to="profile", null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    otp = models.IntegerField(default=0)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

