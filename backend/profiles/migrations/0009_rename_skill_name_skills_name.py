# Generated by Django 3.2.4 on 2021-07-09 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_rename_name_skills_skill_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='skills',
            old_name='skill_name',
            new_name='name',
        ),
    ]
