# Generated by Django 5.0.7 on 2024-07-30 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=20)),
                ('active', models.BooleanField(default=True)),
                ('password', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
