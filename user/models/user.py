from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from user.manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(
        null=True,
        max_length=50,
    )

    last_name = models.CharField(
        null=True,
        max_length=50,
    )

    phone_number = models.CharField(
        null=True,
        max_length=15,
        unique=True,
    )

    password = models.CharField(
        null=True,
        max_length=150,
    )

    email = models.EmailField(
        null=True,
    )

    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        BLOCKED = 'blocked', 'Blocked'

    status = models.CharField(
        max_length=7,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_superuser = models.BooleanField(
        default=False,
    )

    is_admin = models.BooleanField(
        default=False,
    )

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['password']

    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.phone_number
