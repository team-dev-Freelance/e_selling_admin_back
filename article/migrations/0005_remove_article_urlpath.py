# Generated by Django 5.1 on 2024-08-19 15:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_article_urlpath'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='urlPath',
        ),
    ]
