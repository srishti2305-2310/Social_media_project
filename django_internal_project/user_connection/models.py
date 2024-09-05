from django.db import models

from User_Auth.models import User


# Create your models here.


class UserConnection(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending', 'Request Pending'
        APPROVED = 'Accepted', 'Request Accepted'
        REJECTED = 'Rejected', 'Request Rejected'
        BLOCKED = 'Blocked', 'Blocked'

    status = models.CharField(
        max_length=8,
        choices=Status.choices,
        default=Status.PENDING,
    )
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_connections")
    receiver_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_connections")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BlockedUser(models.Model):
    blocker_id = models.ForeignKey(User, related_name="blocked_from", on_delete=models.CASCADE)
    blocked_id = models.ForeignKey(User, related_name="blocked_to", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('blocker_id', 'blocked_id')


class ReportedUser(models.Model):
    reporter_id = models.ForeignKey(User, related_name="reported_by", on_delete=models.CASCADE)
    reported_id = models.ForeignKey(User, related_name="reported_to", on_delete=models.CASCADE)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('reporter_id', 'reported_id')



