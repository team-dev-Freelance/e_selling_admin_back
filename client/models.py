from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from article.models import Article


class ClientManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Le champ email ne peut pas etre vide')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Client(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    active = models.BooleanField(default=True)
    password = models.CharField(max_length=255)
    articles = models.ManyToManyField(Article, blank=False)
    logo = models.ImageField(upload_to='photos/', default='default_logo.png')

    objects = ClientManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def clean(self):
        super().clean()
        if not self.phone.startswith(('62', '65', '67', '68', '69')):
            raise ValueError('Le numéro doit commencer par 62, 65, 67, 68 ou 69.')
        if len(self.phone) != 9 or not self.phone.isdigit():
            raise ValueError('Le numéro de téléphone doit avoir 9 chiffres.')

    def __str__(self):
        return self.email
