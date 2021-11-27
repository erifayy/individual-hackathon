from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from phonenumber_field.modelfields import PhoneNumberField


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError('Phone number must be set.')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError('Phone number must be set.')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.password = make_password(password)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class MyUser(AbstractUser):
    phone_number = PhoneNumberField(unique=True)
    username = models.CharField(max_length=155, unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=6, blank=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()

    def __str__(self):
        return f'{self.username} {self.phone_number}'

    def create_activation_code(self):
        code = get_random_string(length=6, allowed_chars='1234567890AIPERI')
        print(code)
        self.activation_code = code
