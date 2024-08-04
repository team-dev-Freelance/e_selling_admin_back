from django.db import models
from django.utils.translation import gettext_lazy as _

from privilegies.models import Privilegies, Privilege


class Rule(models.TextChoices):
    USER = 'USER', _('User')
    ADMIN = 'ADMIN', _('Admin')
    MEMBER = 'MEMBER', _('Member')


class Role(models.Model):
    role = models.CharField(max_length=20, choices=Rule.choices, default=Rule.USER)
    active = models.BooleanField(default=True)
    privileges = models.ManyToManyField(Privilegies, related_name='privileges')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.privileges.set(self.get_privileges(self.role))

    def get_privileges(self, role=None):
        if role is None:
            role = self.role

        add_privilege = Privilegies.objects.get_or_create(privilege=Privilege.ADD)[0]
        find_privileges = Privilegies.objects.get_or_create(privilege=Privilege.FIND)[0]
        all_privilege = Privilegies.objects.get_or_create(privilege=Privilege.ALL)[0]
        privileges_list = []
        if role in [Rule.ADMIN, Rule.MEMBER]:
            privileges_list.extend([add_privilege, find_privileges])
        if role == Rule.USER:
            privileges_list.append(all_privilege)
        return privileges_list

    def __str__(self):
        return self.role
