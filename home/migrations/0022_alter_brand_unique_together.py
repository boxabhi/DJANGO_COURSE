# Generated by Django 5.0.6 on 2024-06-08 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0021_alter_book_options'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='brand',
            unique_together={('brand_name', 'country')},
        ),
    ]
