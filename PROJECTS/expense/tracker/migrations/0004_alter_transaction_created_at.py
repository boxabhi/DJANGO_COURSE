# Generated by Django 5.0.2 on 2024-06-09 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_remove_transaction_id_alter_transaction_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='created_at',
            field=models.DateField(auto_now=True),
        ),
    ]
