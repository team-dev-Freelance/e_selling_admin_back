from django.db import models

class Role(models.Model):
    role = models.CharField(max_length=20)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.role

