# Generated by Django 5.1.4 on 2024-12-30 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_author_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='name',
            field=models.CharField(db_index=True, max_length=100),
        ),
    ]
