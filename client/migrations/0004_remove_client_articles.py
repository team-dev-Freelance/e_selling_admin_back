# Generated by Django 5.0.7 on 2024-08-04 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_client_logo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='articles',
        ),
    ]