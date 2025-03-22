# Generated by Django 5.1.7 on 2025-03-21 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('active', models.BooleanField(default=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
    ]
