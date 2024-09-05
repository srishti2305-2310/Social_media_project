from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from user_notification.models import Notification
def common_pagination(page, page_size, input_model):
    start = (page - 1) * page_size
    end = start + page_size
    paginated_model = input_model[start:end]
    return paginated_model

def create_notification(sender, receiver, message, notification_type):

    notification = Notification(
        sender=sender,
        receiver=receiver,
        message=message,
        notification_type=notification_type,
        is_read=False
    )
    notification.save()
    return notification