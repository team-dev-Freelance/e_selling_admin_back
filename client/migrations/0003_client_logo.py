# Generated by Django 5.0.7 on 2024-08-03 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_client_articles'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='logo',
            field=models.ImageField(default='default_logo.png', upload_to='photos/'),
        ),
    ]