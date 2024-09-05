from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from User_Auth.models import User
from User_Auth.serializer import LoginSerializer
from user_notification.models import Notification
from utility.api_documantion_helper import send_request_api_doc, withdraw_send_request_api_doc, accept_reject_api_doc, \
block_user_api_doc, report_user_api_doc, list_connection_api_doc, search_username_api_doc, get_profile_view_api_doc


from utility.authentication_helper import is_auth
from utility.email_utils import send_email
from .models import UserConnection, BlockedUser, ReportedUser
from .serializers import UserConnectionSerializer, BlockedUserSerializer, ReportedUserSerializer, \
    ProfileConnectionSerializer
from .validators import verifying_user_connection_request,verifying_accept_reject_request, verifying_user_report
from utility.common_message import CommonMessage
from utility.common_helper import common_pagination
from utility.common_helper import create_notification


@send_request_api_doc
@api_view(['POST'])
@is_auth
def send_request(request):
    if not verifying_user_connection_request(request):
        return Response({"Message": "User not verified"}, status=status.HTTP_400_BAD_REQUEST)

    user_id = request.user_id

    sender = User.objects.get(id=user_id)
    receiver_id = request.data.get('receiver_id')

    try:
        receiver_id = int(receiver_id)
    except ValueError:
        return Response({"error": "Invalid receiver_id format"}, status=status.HTTP_400_BAD_REQUEST)

    receiver = User.objects.filter(id=receiver_id).first()

    if not receiver:
        return Response({"error": "Receiver not found"}, status=status.HTTP_404_NOT_FOUND)

    if UserConnection.objects.filter(sender_id=sender, receiver_id=receiver).exists():
        return Response({"error": "Request already sent"}, status=status.HTTP_400_BAD_REQUEST)

    connection = UserConnection.objects.create(sender_id=sender, receiver_id=receiver)
    serializer = UserConnectionSerializer(connection)

    subject = "New Friend Request"
    plain_text_body = "You have received a new friend request."
    html_template_path = "friend_request_email.html"
    context = {
        "recipient_name": receiver.username,
        "sender_name": sender.username,
        "accept_request_link": "https://example.com/accept-request"
    }
    to_email = receiver.email
    send_email(subject, plain_text_body, html_template_path, context, to_email)
    return Response({"message": CommonMessage.SEND_REQUEST_SUCCESS, "data": serializer.data}, status=status.HTTP_201_CREATED)


@accept_reject_api_doc
@api_view(['POST'])
@is_auth
def handle_friend_request(request):
    if not verifying_accept_reject_request(request):
        return Response({"Message": "User not verified"}, status=status.HTTP_400_BAD_REQUEST)
    sender_id = request.data.get('sender_id')
    action = request.data.get('action')
    user_id = request.user_id

    connection = UserConnection.objects.filter(sender_id=sender_id,receiver_id=user_id,status=UserConnection.Status.PENDING).first()


    if not connection:
        return Response({"error": "Connection request not found."}, status=status.HTTP_404_NOT_FOUND)

    sender = User.objects.get(id=sender_id)
    receiver = User.objects.get(id=user_id)

    if action == 'accept':

        connection.status = UserConnection.Status.APPROVED
        connection.save()


        create_notification(
            sender=receiver,
            receiver=sender,
            message=f"Hi {sender.username}, your friend request to {receiver.username} was accepted!",
            notification_type="Friend Request"
        )

        subject = "Your Friend Request is Accepted!"
        plain_text_body = f"Hi {sender.username}, your friend request to {receiver.username} was accepted!"
        html_template_path = "accept_request_email.html"  # Ensure this template exists
        context = {
            "recipient_name": sender.username,
            "sender_name": receiver.username,
            "connect_profile_link": "https://example.com/connect-profile"  # Replace with actual link
        }
        to_email = sender.email
        send_email(subject, plain_text_body, html_template_path, context, to_email)
        connection.save()

        return Response({"status": "success", "message": CommonMessage.ACCEPT_REQUEST_SUCCESS})

    elif action == 'reject':
        connection.delete()

        return Response({"status": "success", "message":  CommonMessage.REJECT_REQUEST_SUCCESS})


@withdraw_send_request_api_doc
@api_view(['POST'])
@is_auth
def withdraw_send_request(request):
    if not verifying_user_connection_request(request):
        return Response({"Message": "User not verified"}, status=status.HTTP_400_BAD_REQUEST)

    user_id = request.user_id

    sender = User.objects.get(id=user_id)
    receiver_id = request.data.get('receiver_id')

    try:
        receiver_id = int(receiver_id)
    except ValueError:
        return Response({"error": "Invalid receiver_id format"}, status=status.HTTP_400_BAD_REQUEST)

    receiver = User.objects.filter(id=receiver_id).first()

    if not receiver:
        return Response({"error": "Receiver not found"}, status=status.HTTP_404_NOT_FOUND)

    connection = UserConnection.objects.filter(sender_id=sender, receiver_id=receiver)
    connection.delete()
    return Response({"message": CommonMessage.WITHDRAW_REQUEST_SUCCESS}, status=status.HTTP_200_OK)

@list_connection_api_doc
@api_view(['GET'])
@is_auth
def list_connection(request):
    try:
        user_id = request.user_id
        connections_type = request.query_params.get('connections_type')

        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))

        if connections_type == 'blocked':
            blocked_connections = BlockedUser.objects.filter(blocker_id=user_id)
            if not blocked_connections.exists():
                return Response({"message": "No blocked connections found."}, status=status.HTTP_404_NOT_FOUND)

            total_count = blocked_connections.count()
            blocked_connections_paginated = common_pagination(page, page_size, blocked_connections)

            blocked_serializer = BlockedUserSerializer(blocked_connections_paginated, many=True)
            response_data = {
                "count": total_count,
                "blocked_connections": blocked_serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        elif connections_type == 'accepted':
            connections = UserConnection.objects.filter(Q(sender_id=user_id) | Q(receiver_id=user_id), status=UserConnection.Status.APPROVED)

        elif connections_type == 'pending':
            connections = UserConnection.objects.filter(receiver_id=user_id, status=UserConnection.Status.PENDING)

        elif 'friend_id' in request.query_params:
            user_id = request.query_params.get('friend_id')
            friends = UserConnection.objects.filter(Q(sender_id=user_id) | Q(receiver_id=user_id), status=UserConnection.Status.APPROVED)
            if not friends.exists():
                return Response({"message": "No friends found."}, status=status.HTTP_404_NOT_FOUND)

            total_count = friends.count()
            friends_paginated = common_pagination(page, page_size, friends)
            serializer = UserConnectionSerializer(friends_paginated, many=True)
            response_data = {
                "count": total_count,
                "data": serializer.data,
            }
            return Response(response_data, status=status.HTTP_200_OK)

        else:
            return Response({"error": "Invalid connection type provided."}, status=status.HTTP_400_BAD_REQUEST)

        if not connections.exists():
            return Response({"message": f"No {connections_type} connection requests found."},
                            status=status.HTTP_404_NOT_FOUND)

        total_count = connections.count()
        connections_paginated = common_pagination(page, page_size, connections)

        serializer = UserConnectionSerializer(connections_paginated, many=True)
        response_data = {
            "count": total_count,
            "data": serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@block_user_api_doc
@api_view(['POST'])
@is_auth
def block_user(request):
    user_id = request.user_id
    blocked_user_id = request.data.get('blocked_user_id')

    try:
        blocked_user_id = int(blocked_user_id)
    except ValueError:
        return Response({"error": "value is not a valid integer, give correct blocked_user_id"},
                        status=status.HTTP_400_BAD_REQUEST)

    blocked_user = User.objects.filter(id=blocked_user_id).first()

    if not blocked_user:
        return Response({"error": "User blocked does not exist"}, status=status.HTTP_404_NOT_FOUND)

    if BlockedUser.objects.filter(blocker_id=user_id, blocked_id=blocked_user_id).exists():
        return Response({"error": "User is already blocked"}, status=status.HTTP_400_BAD_REQUEST)

    block_entry = BlockedUser.objects.create(blocker_id_id=user_id, blocked_id_id=blocked_user_id)
    serializer = BlockedUserSerializer(block_entry)

    return Response({"message": CommonMessage.BLOCK_USER_SUCCESS, "data": serializer.data}, status=status.HTTP_201_CREATED)


@report_user_api_doc
@api_view(['POST'])
@is_auth
def report_user(request):
    if not verifying_user_report(request):
        return Response({"message": "Report user not verified"}, status=status.HTTP_400_BAD_REQUEST)

    user_id = request.user_id
    reported_user_id = request.data.get('reported_user_id')
    reason = request.data.get('reason')

    try:
        reported_user_id = int(reported_user_id)
    except ValueError:
        return Response({"error": "Reported user id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)

    reported_user = User.objects.filter(id=reported_user_id).first()
    if not reported_user:
        return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

    # Check if the user has already reported
    if ReportedUser.objects.filter(reporter_id=user_id, reported_id=reported_user_id).exists():
        return Response({"error": "You have already reported this user"}, status=status.HTTP_400_BAD_REQUEST)

    # Create the report entry
    report_entry = ReportedUser.objects.create(reporter_id_id=user_id, reported_id_id=reported_user_id, reason=reason)
    serializer = ReportedUserSerializer(report_entry)

    return Response({"message": CommonMessage.REPORT_USER_SUCCESS, "data": serializer.data},
                    status=status.HTTP_201_CREATED)

@search_username_api_doc
@api_view(['GET'])
@is_auth
def search_username(request):
    try:
        search_username = request.query_params.get('username')
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))

        users = User.objects.filter(username__icontains=search_username)

        paginated_users = common_pagination(page, page_size, users)
        total_count = users.count()

        serializer = LoginSerializer(paginated_users, many=True)
        response_data = {
            "count": total_count,
            "data": serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@get_profile_view_api_doc
@api_view(['GET'])
@is_auth
def get_profile_view(request):
    user_id = request.user_id
    connection_id = request.query_params.get("connection_id")
    page = int(request.query_params.get('page', 1))
    page_size = int(request.query_params.get('page_size', 10))

    try:
        user = User.objects.get(id=connection_id)

        connection = UserConnection.objects.filter(
            (Q(sender_id=user_id) & Q(receiver_id=connection_id)) |
            (Q(sender_id=connection_id) & Q(receiver_id=user_id)),
            status=UserConnection.Status.APPROVED
        ).first()

        if not connection:
            return Response({"username": user.username}, status=status.HTTP_200_OK)

        connections = UserConnection.objects.filter(
            (Q(sender_id=user_id) | Q(receiver_id=user_id)),
            status=UserConnection.Status.APPROVED
        )

        paginated_connections = common_pagination(page, page_size, connections)
        total_count = connections.count()

        connection_serializer = UserConnectionSerializer(paginated_connections, many=True)
        profile_serializer = ProfileConnectionSerializer(user)

        response_data = {
            "profile": profile_serializer.data,
            "connections_count": total_count,
            "connections": connection_serializer.data,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"error": "User Not Found"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)