# Generated by Django 5.1 on 2024-09-26 12:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('article', '0005_remove_article_urlpath'),
        ('utilisateur', '0003_remove_utilisateur_logo_name_alter_utilisateur_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_command', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'En cours'), ('shipped', 'Expédiée'), ('delivered', 'Livrée')], max_length=20)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utilisateur.client')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article.article')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='articles',
            field=models.ManyToManyField(through='order.OrderItem', to='article.article'),
        ),
    ]
