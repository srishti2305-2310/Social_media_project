# Generated by Django 5.0.7 on 2024-08-12 10:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User_Auth', '0002_u_security_q'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersecurityQuestion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('security_q', models.CharField(max_length=200)),
                ('security_a', models.CharField(max_length=200)),
                ('user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='User_Auth.user')),
            ],
        ),
        migrations.DeleteModel(
            name='U_security_q',
        ),
    ]
