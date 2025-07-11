from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("student", "Student"),
        ("teacher", "Teacher"),
    )
    # Add the role field with choices and a default
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")
