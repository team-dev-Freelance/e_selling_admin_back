# Generated by Django 5.0.7 on 2024-08-09 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateur', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='client',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='member',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='member',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
