# Generated by Django 5.0.2 on 2024-06-24 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('category', models.CharField(max_length=100)),
                ('price', models.FloatField()),
                ('brand', models.CharField(blank=True, max_length=100, null=True)),
                ('sku', models.CharField(max_length=100)),
                ('thumbnail', models.URLField(max_length=1000)),
                ('tags', models.ManyToManyField(to='products.tags')),
            ],
        ),
    ]