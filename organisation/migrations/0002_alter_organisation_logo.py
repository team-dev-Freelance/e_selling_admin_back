# Generated by Django 5.0.7 on 2024-08-03 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='logo',
            field=models.ImageField(default='default_logo.png', upload_to='photos/'),
        ),
    ]
