# Generated by Django 5.0.2 on 2024-06-23 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='otp',
            field=models.IntegerField(default=0),
        ),
    ]
