import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from User_Auth.models import User
from user_connection.models import UserConnection
from user_notification.models import Notification
from django.utils import timezone

def send_birthday_reminders():
    try:
        today = timezone.now().date()
        birthday_users = User.objects.filter(dob=today)
        for user in birthday_users:
            sender_friends_ids = UserConnection.objects.filter(
                sender_id=user.id,
                status='Accepted'
            ).values_list('receiver_id', flat=True)

            receiver_friends_ids = UserConnection.objects.filter(
                receiver_id=user.id,
                status='Accepted'
            ).values_list('sender_id', flat=True)

            friends_ids = set(sender_friends_ids) | set(receiver_friends_ids)
            friends = User.objects.filter(id__in=friends_ids).distinct()
            for friend in friends:
                notification = Notification(
                    sender=user,
                    receiver=friend,
                    message=f"Today is {user.username}'s birthday!",
                    notification_type='Reminder',
                )
                notification.save()

    except Exception as e:
        print(f"An error occurred in send_birthday_reminders: {e}")


def start_scheduler():
    scheduler = BackgroundScheduler()
    trigger_time = datetime.datetime.now() + datetime.timedelta(minutes=1)
    scheduler.add_job(
        send_birthday_reminders,
        trigger=DateTrigger(run_date=trigger_time),
        id='birthday_reminder_job',
        max_instances=1,
        replace_existing=True,
    )
    scheduler.start()
    job = scheduler.get_job('birthday_reminder_job')
    if job:
        print(f"Job added successfully: {job}")
    else:
        print("Job not added.")

start_scheduler()
