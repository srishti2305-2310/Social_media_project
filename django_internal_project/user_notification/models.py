from django.db import models

from User_Auth.models import User

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('Friend_Request', 'Friend Request'),
        ('Message', 'Message'),
        ('Reminder', 'Reminder'),
        ('Tag_Wish', 'Tag Wish')
    ]

    sender = models.ForeignKey(User, related_name='sent_notifications', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_notifications', on_delete=models.CASCADE)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
