# Generated by Django 5.1.4 on 2024-12-30 10:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_student_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'default_related_name': 'books'},
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.author'),
        ),
    ]
