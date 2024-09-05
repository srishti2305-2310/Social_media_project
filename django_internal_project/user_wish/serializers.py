from rest_framework import serializers
from .models import UserWish


class UserWishSerializers(serializers.ModelSerializer):
    tag_username = serializers.CharField(source='tag_id.username', read_only=True)

    class Meta:
        model=UserWish
        fields="__all__"
