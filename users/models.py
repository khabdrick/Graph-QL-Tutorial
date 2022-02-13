from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(blank=False, verbose_name="Email")

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
