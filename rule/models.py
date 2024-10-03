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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.role

