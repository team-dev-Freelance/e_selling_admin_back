# Generated by Django 5.1 on 2024-08-19 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_alter_article_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='urlPath',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
