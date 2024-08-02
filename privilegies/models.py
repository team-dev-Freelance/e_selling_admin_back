from django.db import models
from django.utils.translation import gettext_lazy as _

#from rule.models import Role


class Privilege(models.TextChoices):
    ADD = 'ADD', _('Add')
    DELETE = 'DELETE', _('Delete')
    UPDATE = 'UPDATE', _('Update')
    ALL = 'ALL', _('All')
    FIND = 'FIND', _('Find')


class Privilegies(models.Model):
    privilege = models.CharField(max_length=20, choices=Privilege.choices, default=Privilege.FIND)
    active = models.BooleanField(default=True)
#    role = models.ManyToManyField(Role, related_name='privileges')

    def __str__(self):
        return self.privilege
