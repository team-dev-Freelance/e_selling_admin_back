from django.db import models
from django.utils.translation import gettext_lazy as _

from privilegies.models import Privilegies


class Rule(models.TextChoices):
    USER = 'USER', _('User')
    ADMIN = 'ADMIN', _('Admin')
    MEMBER = 'MEMBER', _('Member')


class Role(models.Model):
    role = models.CharField(max_length=20, choices=Rule.choices, default=Rule.USER)
    active = models.BooleanField(default=True)
    privileges = models.ManyToManyField(Privilegies, related_name='privileges')

    def __str__(self):
        return self.role
