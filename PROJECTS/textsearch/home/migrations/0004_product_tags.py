# Generated by Django 5.0.6 on 2024-06-17 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_tags_alter_product_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(to='home.tags'),
        ),
    ]
