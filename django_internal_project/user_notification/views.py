from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.decorators import api_view
from utility.authentication_helper import is_auth
from user_notification.models import Notification

def index(request):
    return HttpResponse("Welcome to Notification Page.")
@api_view(['POST'])
@is_auth
def mark_notification_as_read_or_delete(request, notification_id, action):
    try:
        notification = Notification.objects.get(id=notification_id, receiver=request.user_id)

        if action == 'read':
            notification.is_read = True
            notification.save()
            return Response({"status": "success", "message": "Notification marked as read."})

        elif action == 'delete':
            notification.delete()
            return Response({"status": "success", "message": "Notification deleted."})

        else:
            return Response({"error": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)
    except Notification.DoesNotExist:
        return Response({"error": "Notification not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@is_auth
def list_notifications(request):

    user_id = request.user_id
    notifications = Notification.objects.filter(receiver_id=user_id).order_by('-created_at')

    page_number = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))

    start = (page_number - 1) * page_size
    end = start + page_size

    paginated_notifications = notifications[start:end]

    serializer = NotificationSerializer(paginated_notifications, many=True)

    paginated_data = {
        'count': notifications.count(),
        'total_pages': (notifications.count() + page_size - 1) // page_size,
        'current_page': page_number,
        'notifications': serializer.data
    }

    return Response(paginated_data, status=status.HTTP_200_OK)

