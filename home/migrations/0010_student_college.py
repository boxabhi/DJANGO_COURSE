# Generated by Django 5.0.6 on 2024-06-02 08:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_college'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='college',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.college'),
        ),
    ]
