# Generated by Django 3.2.4 on 2021-07-09 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_auto_20210709_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(blank=True, null=True, related_name='personal_skills', to='profiles.Skills'),
        ),
    ]