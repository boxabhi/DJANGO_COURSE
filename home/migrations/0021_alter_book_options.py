# Generated by Django 5.0.6 on 2024-06-08 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_alter_book_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ('-price', 'book_name'), 'verbose_name': 'Book', 'verbose_name_plural': 'Book'},
        ),
    ]