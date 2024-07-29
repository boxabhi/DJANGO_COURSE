# Generated by Django 5.0.2 on 2024-06-13 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('category', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('brand', models.CharField(max_length=100)),
                ('sku', models.CharField(max_length=100)),
                ('thumbnail', models.URLField(max_length=10000)),
            ],
        ),
    ]
