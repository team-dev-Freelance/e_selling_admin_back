import os

from cloudinary.models import CloudinaryField
from django.db import models


class Organisation(models.Model):
    label = models.CharField(max_length=255)
    description = models.TextField()
    createDate = models.DateField(auto_now_add=True, editable=False)
    active = models.BooleanField(default=True)
    phone = models.CharField(max_length=20, default='')
    logo = models.ImageField(upload_to='photos/', default='media/photos/logo.jpeg')
    # logo = models.ImageField(upload_to='photos/', default='default_logo.png')
    # logo_name = models.CharField(max_length=255, blank=True)
    #
    # def save(self, *args, **kwargs):
    #     if self.logo:
    #         self.logo_name = os.path.basename(self.logo.name)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.label

    # def clean(self):
    #     super().clean()
    #     if not self.phone.startswith(('65', '67', '68', '69')):
    #         raise ValueError('Le numéro doit commencer par 65, 67, 68 ou 69.')
    #     if len(self.phone) != 9 or not self.phone.isdigit():
    #         raise ValueError('Le numéro de téléphone doit avoir 9 chiffres.')

