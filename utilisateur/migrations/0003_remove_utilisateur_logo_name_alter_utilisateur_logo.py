# Generated by Django 5.1 on 2024-08-17 14:06

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateur', '0002_utilisateur_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='utilisateur',
            name='logo_name',
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='logo',
            field=cloudinary.models.CloudinaryField(default='media/photos/logo.jpeg', max_length=255, verbose_name='image'),
        ),
    ]
