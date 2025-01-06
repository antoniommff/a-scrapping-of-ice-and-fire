from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class CustomUserManager(BaseUserManager):

    def create_user(self, name, surname, email, username,
                    password, **extra_fields):
        if not name:
            raise ValueError('El nombre es obligatorio')
        if not surname:
            raise ValueError('Los apellidos son obligatorios')
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        if not username:
            raise ValueError('El nombre de usuario es obligatorio')
        if not password:
            raise ValueError('La contraseña es obligatoria')

        user = self.model(
            name=name,
            surname=surname,
            email=self.normalize_email(email),
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, surname, email, username,
                         password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(name, surname, email, username,
                                password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'surname', 'email', 'password']

    def __str__(self):
        return f"{self.name} {self.surname} ({self.username})"
