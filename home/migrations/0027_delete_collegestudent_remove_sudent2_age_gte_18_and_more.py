# Generated by Django 5.0.2 on 2024-08-03 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_collegestudent_skills_is_deleted'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CollegeStudent',
        ),
        migrations.RemoveConstraint(
            model_name='sudent2',
            name='age_gte_18',
        ),
        migrations.RemoveField(
            model_name='student',
            name='age',
        ),
    ]