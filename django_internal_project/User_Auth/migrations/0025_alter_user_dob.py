# Generated by Django 5.0.7 on 2024-08-13 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_Auth', '0024_alter_user_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dob',
            field=models.CharField(blank=True, default=None, max_length=20, null=True),
        ),
    ]
