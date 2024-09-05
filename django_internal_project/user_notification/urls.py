from django.urls import path
from user_notification.views import index, mark_notification_as_read_or_delete, list_notifications

urlpatterns = [
    path('', index, name='notification'),
    path('notification/<int:notification_id>/<str:action>/', mark_notification_as_read_or_delete, name='mark_notification_as_read_or_delete'),
    path('notification-list/', list_notifications, name='notification-list'),
]
