# Generated by Django 5.0.7 on 2024-08-03 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_remove_article_clients_article_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='logo',
            field=models.ImageField(default='default_logo.png', upload_to='photos/'),
        ),
    ]
