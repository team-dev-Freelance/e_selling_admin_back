from django.db import models
from django.utils.translation import gettext_lazy as _

from privilegies.models import Privilegies, Privilege


class Rule(models.TextChoices):
    USER = 'USER', _('User')
    ADMIN = 'ADMIN', _('Admin')
    MEMBER = 'MEMBER', _('Member')
    CLIENT = 'CLIENT', _('Client')


class Role(models.Model):
    role = models.CharField(max_length=20, choices=Rule.choices)
    active = models.BooleanField(default=True)
    # privileges = models.ManyToManyField(Privilegies, related_name='roles')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Assurez-vous de ne pas utiliser `set()` dans `save()`
        # Utilisez-le lors de la création ou mise à jour des objets
        # self.privileges.set(self.get_privileges(self.role))

    # def get_privileges(self, role=None):
    #     if role is None:
    #         role = self.role
    #
    #     add_privilege, _ = Privilegies.objects.get_or_create(privilege=Privilege.ADD)
    #     find_privileges, _ = Privilegies.objects.get_or_create(privilege=Privilege.FIND)
    #     all_privilege, _ = Privilegies.objects.get_or_create(privilege=Privilege.ALL)
    #     privileges_list = []
    #     if role in [Rule.ADMIN, Rule.MEMBER]:
    #         privileges_list.extend([add_privilege, find_privileges])
    #     if role == Rule.USER:
    #         privileges_list.append(all_privilege)
    #     if role == Rule.CLIENT:
    #         privileges_list.append(find_privileges)
    #     return privileges_list

    def __str__(self):
        return self.role

