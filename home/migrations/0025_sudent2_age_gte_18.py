# Generated by Django 5.0.6 on 2024-06-08 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_engineer_hr_investors'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='sudent2',
            constraint=models.CheckConstraint(check=models.Q(('age__gte', 18)), name='age_gte_18'),
        ),
    ]