import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from rule.models import Role
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Le champ email ne peut pas être vide!')
        user = self.model(email=email, **extra_fields)
        user.set_password(password) # Hachage du mot de passe
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if 'rule' not in extra_fields:
            role, created = Role.objects.get_or_create(
                role='ADMIN',
            )
            if created:
                role.save()
            extra_fields['rule'] = role
        return self.create_user(email, password, **extra_fields)


class Utilisateur(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20,  blank=True)
    active = models.BooleanField(default=True)
    rule = models.ForeignKey(Role, on_delete=models.CASCADE, null=False, blank=False) 
    logo = models.ImageField(upload_to='photos/', default='media/photos/logo.jpeg')
    # status = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    
    def __str__(self):
        return self.email
    def clean(self):
        super().clean()
        if not self.phone.startswith(('65', '67', '68', '69')):
            raise ValueError('Le numéro doit commencer par 65, 67, 68 ou 69.')
        if len(self.phone) != 9 or not self.phone.isdigit():
            raise ValueError('Le numéro de téléphone doit avoir 9 chiffres.')

    def __str__(self):
        return self.email



class Client(Utilisateur):
    class Meta:
        db_table = 'client'


class Member(Utilisateur):
   
    class Meta:
        db_table = 'member'


