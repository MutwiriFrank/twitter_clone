# Generated by Django 3.2.4 on 2021-07-09 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_alter_profile_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='other_skills',
            field=models.CharField(blank=True, max_length=220, null=True),
        ),
    ]
