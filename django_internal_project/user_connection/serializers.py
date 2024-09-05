from rest_framework import serializers

from User_Auth.models import User
from user_wish.serializers import UserWishSerializers
from .models import UserConnection, BlockedUser, ReportedUser


class UserConnectionSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender_id.username', read_only=True)
    receiver_username = serializers.CharField(source='receiver_id.username', read_only=True)

    class Meta:
        model = UserConnection
        fields = "__all__"




class ProfileConnectionSerializer(serializers.ModelSerializer):
    user_wishes = UserWishSerializers(many=True)

    class Meta:
        model = User
        fields = ['id','username', 'first_name', 'last_name', 'gender', 'dob', 'phone_no', 'user_wishes']




class BlockedUserSerializer(serializers.ModelSerializer):
    blocker_username = serializers.CharField(source='blocker_id.username', read_only=True)
    blocked_username = serializers.CharField(source='blocked_id.username', read_only=True)

    class Meta:
        model = BlockedUser
        fields = ['id', 'blocker_id', 'blocker_username', 'blocked_id', 'blocked_username', 'created_at']


class ReportedUserSerializer(serializers.ModelSerializer):
    reporter_username = serializers.CharField(source='reporter_id.username', read_only=True)
    reported_username = serializers.CharField(source='reported_id.username', read_only=True)
    # report_count = serializers.SerializerMethodField()

    class Meta:
        model = ReportedUser
        fields = "__all__"



