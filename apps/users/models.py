from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    SUPER_ADMIN = "SUPER_ADMIN"
    COUNTRY_ADMIN = "COUNTRY_ADMIN"
    COUNTRY_MEMBER = "COUNTRY_MEMBER"

    ROLE_CHOICES = (
        (SUPER_ADMIN, "Super Admin"),
        (COUNTRY_ADMIN, "Country Admin"),
        (COUNTRY_MEMBER, "Country Member"),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=COUNTRY_MEMBER)
    country = models.CharField(max_length=100, blank=True, null=True)

    REQUIRED_FIELDS = ["email", "role", "country"]

    def __str__(self):
        return f"{self.username} ({self.role}) - {self.country or 'N/A'}"
