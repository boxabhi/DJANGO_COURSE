# Generated by Django 5.0.6 on 2024-06-08 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_delete_mymodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField()),
            ],
        ),
    ]
