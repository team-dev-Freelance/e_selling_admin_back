# member/models.py
import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission

from organisation.models import Organisation
from privilegies.models import Privilegies, Privilege
from rule.models import Role
from utilisateur.models import User


# class MemberManager(BaseUserManager):
#     def create_user(self, username, password=None, **extra_fields):
#         if not username:
#             raise ValueError('Le champ username ne peut pas être vide!')
#         user = self.model(username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, username, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#
#         # Assurez-vous que l'instance Privilegies pour 'ALL' existe
#         all_privilege, created = Privilegies.objects.get_or_create(privilege=Privilege.ALL)
#
#         if 'rule' not in extra_fields:
#             # Créez ou obtenez l'objet Role avec le privilège ALL
#             role, created = Role.objects.get_or_create(
#                 role='ADMIN',
#                 active=True
#             )
#             if created:
#                 role.privileges.set([all_privilege])
#                 role.save()
#             extra_fields['rule'] = role
#
#         if 'organisation' not in extra_fields:
#             # Créez ou obtenez l'objet Organisation
#             organisation, created = Organisation.objects.get_or_create(
#                 label='Organisation',
#                 defaults={'active': False}
#             )
#             extra_fields['organisation'] = organisation
#
#         return self.create_user(username, password, **extra_fields)


# class Member(User):
#     # username = models.CharField(max_length=255, unique=True)
#     # email = models.EmailField(unique=True)
#     # phone = models.CharField(max_length=20)
#     # # password = models.
#     # active = models.BooleanField(default=True)
#     # is_staff = models.BooleanField(default=False)
#     # is_superuser = models.BooleanField(default=False)
#     organisation = models.ForeignKey('organisation.Organisation', related_name='members', on_delete=models.CASCADE,
#                                      null=True, blank=False)
    # rule = models.ForeignKey('rule.Role', on_delete=models.CASCADE, null=True, blank=False)
    # logo = models.ImageField(upload_to='photos/', default='default_logo.png')
    # logo_name = models.CharField(max_length=255, blank=True)
    # groups = models.ManyToManyField(Group, related_name='member_set', blank=True)
    # user_permissions = models.ManyToManyField(Permission, related_name='member_user_permissions', blank=True)
    #
    # objects = MemberManager()
    #
    # USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['email']
    #
    # def save(self, *args, **kwargs):
    #     if self.logo:
    #         self.logo_name = os.path.basename(self.logo.name)
    #     super().save(*args, **kwargs)
    #
    # def clean(self):
    #     super().clean()
    #     if not self.phone.startswith(('62', '65', '67', '68', '69')):
    #         raise ValueError('Le numéro doit commencer par 62, 65, 67, 68 ou 69.')
    #     if len(self.phone) != 9 or not self.phone.isdigit():
    #         raise ValueError('Le numéro de téléphone doit avoir 9 chiffres.')
    #
    # def __str__(self):
    #     return self.username
