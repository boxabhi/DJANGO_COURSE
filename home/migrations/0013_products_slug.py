# Generated by Django 5.0.6 on 2024-06-08 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_alter_book_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, null=True),
        ),
    ]