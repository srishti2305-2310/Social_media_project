from django.db import models

from User_Auth.models import User


# Create your models here.

class UserWish(models.Model):
    userwish_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_wishes")
    tag_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tagged_wishes")
    title = models.CharField(max_length=200, null=True)
    description = models.CharField(max_length=200, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

