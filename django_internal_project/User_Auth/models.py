from django.contrib.auth.hashers import check_password, make_password
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, default=None, blank=True, null=True)
    last_name = models.CharField(max_length=50, default=None, blank=True, null=True)
    gender = models.CharField(max_length=10, default=None, blank=True, null=True)
    dob = models.DateField(null=True, default=None, blank=True)
    password = models.CharField(max_length=500)
    phone_no = models.BigIntegerField(null=True, default=None, blank=True)
    refresh_token = models.CharField(max_length=200, default='None')
    is_login = models.BooleanField(default=False)
    is_block = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def total_reports(self):
        return self.reported_to.count()

    total_reports.short_description = 'Total Reports'


class UsersecurityQuestion(models.Model):
    id = models.AutoField(primary_key=True, serialize=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    security_q = models.CharField(max_length=200, null=True)
    security_a = models.CharField(max_length=200)

    def __str__(self):
        return self.security_q
