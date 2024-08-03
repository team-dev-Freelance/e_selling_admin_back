from django.db import models


class Organisation(models.Model):
    label = models.CharField(max_length=255)
    description = models.TextField()
    createDate = models.DateField(auto_now_add=True, editable=False)
    active = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='photos/', default='default_logo.png')

    def __str__(self):
        return self.label
