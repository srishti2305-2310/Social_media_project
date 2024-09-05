from functools import wraps

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from User_Auth.serializer import LoginSerializer


from User_Auth.serializer import LoginSerializer


def signup_api_doc(func):
    @swagger_auto_schema(
        method='post',
        operation_description="User create a account",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username for the new account'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address for the new account'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password for the new account'),
                'security_q': openapi.Schema(type=openapi.TYPE_STRING, description='Security question for the account'),
                'security_a': openapi.Schema(type=openapi.TYPE_STRING, description='Answer to the security question'),
            },
            required=['username', 'password', 'security_q', 'security_a']
        ),
        responses={
            200: openapi.Response(
                description='User Created Successfully',
                examples={
                    'application/json': {
                        'Success': 'User Created Successfully'
                    }
                }
            ),
            400: openapi.Response(
                description='Invalid request body',
                examples={
                    'application/json': {
                        'Error': 'Invalid request body'
                    }
                }
            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def login_api_doc(func):
    @swagger_auto_schema(
        method='post',
        operation_description="User login",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username or email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password')
            },
            required=['username', 'password']
        ),
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING, description='Access token'),
                        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token'),
                        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                        'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email')
                    }
                )
            ),
            400: openapi.Response(
                description="Invalid data"
            ),
            401: openapi.Response(
                description="Invalid credentials or incorrect password"
            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def logout_api_doc(func):
    @swagger_auto_schema(
        method='post',
        operation_description="User logout",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token')
            },
            required=['refresh_token']
        ),
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Logout successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message')
                    }
                ),
                examples={
                    'application/json': {
                        'message': 'Logout successful'
                    }
                }
            ),
            400: openapi.Response(
                description="Invalid data",
                examples={
                    'application/json': {
                        'error': 'Invalid data'
                    }
                }
            ),
            401: openapi.Response(
                description="Authorization Token is missing or invalid",
                examples={
                    'application/json': {
                        'error': 'Authorization Token is missing!'
                    }
                }
            ),
            403: openapi.Response(
                description="Permission denied",
                examples={
                    'application/json': {
                        'error': 'Permission denied'
                    }
                }
            ),
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def forgot_api_doc(func):
    @swagger_auto_schema(
        method='post',
        operation_description="Forgot password",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username or email'),
                'security_q': openapi.Schema(type=openapi.TYPE_STRING, description='Security question'),
                'security_a': openapi.Schema(type=openapi.TYPE_STRING, description='Answer to the security question'),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='New password')
            },
            required=['username', 'security_q', 'security_a', 'new_password']
        ),
        responses={
            200: openapi.Response(
                description='Password reset successfully',
                examples={
                    'application/json': {
                        'success': True,
                        'message': 'Password reset successfully'
                    }
                }
            ),
            400: openapi.Response(
                description='Invalid data',
                examples={
                    'application/json': {
                        'success': False,
                        'message': 'Invalid data'
                    }
                }
            ),
            404: openapi.Response(
                description='User or security question not found',
                examples={
                    'application/json': {
                        'error': 'User not found or security question not found'
                    }
                }
            ),
            401: openapi.Response(
                description='Incorrect security question or answer',
                examples={
                    'application/json': {
                        'error': 'Security question or answer is incorrect'
                    }
                }
            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def update_security_api_doc(func):
    @swagger_auto_schema(
        method='put',
        operation_description="Update security question and answer",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username or email'),
                'security_q': openapi.Schema(type=openapi.TYPE_STRING, description='Security question'),
                'security_a': openapi.Schema(type=openapi.TYPE_STRING, description='Answer to the security question'),
            },
            required=['username', 'security_q', 'security_a']
        ),
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description='Security question and answer updated successfully',
                examples={
                    'application/json': {
                        'success': True,
                        'message': 'Security question and answer updated successfully'
                    }
                }
            ),
            400: openapi.Response(
                description='Both security question and answer are required',
                examples={
                    'application/json': {
                        'error': 'Both security question and answer are required'
                    }
                }
            ),
            401: openapi.Response(
                description='Authorization token is missing or invalid',
                examples={
                    'application/json': {
                        'error': 'Authorization Token is missing!'
                    }
                }
            ),
            403: openapi.Response(
                description='User does not have permission to update security question',
                examples={
                    'application/json': {
                        'error': 'Permission denied'
                    }
                }
            ),
            404: openapi.Response(
                description='User or security question not found',
                examples={
                    'application/json': {
                        'error': 'User not found'  # Or 'Security question not found' if appropriate
                    }
                }
            ),
            500: openapi.Response(
                description='Internal server error',

            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def get_security_api_doc(func):
    @swagger_auto_schema(
        method='get',
        operation_description="Retrieve the security question and answer for the user",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Page number for pagination (default: 1)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'page_size',
                openapi.IN_QUERY,
                description="Number of results per page for pagination (default: 10)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
        ],
        responses={
            200: openapi.Response(
                description='Security question and answer retrieved successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'security_q': openapi.Schema(type=openapi.TYPE_STRING, description='Security question'),
                        'security_a': openapi.Schema(type=openapi.TYPE_STRING,
                                                     description='Answer to the security question'),
                    }
                ),
                examples={
                    'application/json': {
                        'security_q': 'What is your mother\'s maiden name?',
                        'security_a': 'Smith'
                    }
                }
            ),
            404: openapi.Response(
                description='User or security question not found',
                examples={
                    'application/json': {
                        'error': 'User not found'
                    }
                }
            ),
            500: openapi.Response(
                description='Internal server error',
                examples={
                    'application/json': {
                        'error': 'An unexpected error occurred'
                    }
                }
            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def update_profile_api_doc(func):
    @swagger_auto_schema(
        method='put',
        operation_description="Update user profile information",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='User first name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='User last name'),
                'gender': openapi.Schema(type=openapi.TYPE_STRING, description='User gender'),
                'dob': openapi.Schema(type=openapi.TYPE_STRING, description='User date of birth',
                                      format=openapi.FORMAT_DATE),
                'phone_no': openapi.Schema(type=openapi.TYPE_STRING, description='User phone number'),
            },
            required=['first_name', 'last_name', 'gender', 'dob', 'phone_no']
        ),
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description='Profile updated successfully',
                examples={
                    'application/json': {
                        'Success': 'Profile Updated Successfully'
                    }
                }
            ),
            400: openapi.Response(
                description='Invalid input data',
                examples={
                    'application/json': {
                        'error': 'Invalid input data'
                    }
                }
            ),
            401: openapi.Response(
                description='Authorization Token is missing or invalid',
                examples={
                    'application/json': {
                        'error': 'Authorization Token is missing!'
                    }
                }
            ),
            404: openapi.Response(
                description='User not found',
                examples={
                    'application/json': {
                        'error': 'User not found'
                    }
                }
            ),
            500: openapi.Response(
                description='Internal server error',
                examples={
                    'application/json': {
                        'error': 'An unexpected error occurred'
                    }
                }
            ),
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def get_profile_api_doc(func):
    @swagger_auto_schema(
        method='get',
        operation_description="Retrieve user profile information",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Page number for pagination (default: 1)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'page_size',
                openapi.IN_QUERY,
                description="Number of results per page for pagination (default: 10)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
        ],
        responses={
            200: openapi.Response(
                description='User profile retrieved successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
                        'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                        'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                        'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='User first name'),
                        'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='User last name'),
                        'gender': openapi.Schema(type=openapi.TYPE_STRING, description='User gender'),
                        'dob': openapi.Schema(type=openapi.TYPE_STRING, description='User date of birth',
                                              format=openapi.FORMAT_DATE),
                        'phone_no': openapi.Schema(type=openapi.TYPE_STRING, description='User phone number'),
                        'created_at': openapi.Schema(type=openapi.TYPE_STRING, description='Account creation date',
                                                     format=openapi.FORMAT_DATETIME),
                        'updated_at': openapi.Schema(type=openapi.TYPE_STRING, description='Last update date',
                                                     format=openapi.FORMAT_DATETIME),
                    }
                ),
            ),
            401: openapi.Response(
                description='Unauthorized or invalid token',
                examples={
                    'application/json': {
                        'error': 'Authorization Token is missing or invalid'
                    }
                }
            ),
            404: openapi.Response(
                description='User not found',
                examples={
                    'application/json': {
                        'error': 'User not found'
                    }
                }
            ),
            500: openapi.Response(
                description='Internal server error',
                examples={
                    'application/json': {
                        'error': 'An unexpected error occurred'
                    }
                }
            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def user_delete_api_doc(func):
    @swagger_auto_schema(
        method='delete',
        operation_description="Delete a user account",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description='User deleted successfully',
                examples={
                    'application/json': {
                        'success': True,
                        'message': 'User deleted successfully'
                    }
                }
            ),
            404: openapi.Response(
                description='User not found',
                examples={
                    'application/json': {
                        'success': False,
                        'error': 'User not found'
                    }
                }
            ),
            500: openapi.Response(
                description='Internal server error',
                examples={
                    'application/json': {
                        'success': False,
                        'error': 'An unexpected error occurred'
                    }
                }
            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def get_refresh_token_api_doc(func):
    @swagger_auto_schema(
        method='post',
        operation_description="Retrieve new access and refresh tokens using a refresh token",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING,
                                                description='The refresh token used to generate new tokens'),
            },
            required=['refresh_token']
        ),
        responses={
            200: openapi.Response(
                description='Successfully generated new tokens',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='New refresh token'),
                        'access_token': openapi.Schema(type=openapi.TYPE_STRING, description='New access token'),
                    }
                ),
                examples={
                    'application/json': {
                        'refresh_token': 'new_refresh_token_value',
                        'access_token': 'new_access_token_value'
                    }
                }
            ),
            400: openapi.Response(
                description='Invalid request body',
                examples={
                    'application/json': {
                        'Error': 'Invalid Request Body'
                    }
                }
            ),
            401: openapi.Response(
                description='Unauthorized or invalid refresh token',
                examples={
                    'application/json': {
                        'Error': 'Unauthorized or invalid refresh token'
                    }
                }
            ),
            500: openapi.Response(
                description='Internal server error',
                examples={
                    'application/json': {
                        'Error': 'An unexpected error occurred'
                    }
                }
            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def send_request_api_doc(func):
    @swagger_auto_schema(
        method='post',
        operation_description="Sending connection request for the user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'receiver_id': openapi.Schema(type=openapi.TYPE_INTEGER,
                                              description='The receiver_id gives us the receivers user_id '),
            },
            required=['receiver_id']
        ),
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description='Successfully Send Conncetion Request',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'receiver_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='New refresh token'),

                    }
                ),
                examples={
                    'application/json': {
                        'message': 'Request sent Successfully',

                    }
                }
            ),
            400: openapi.Response(
                description='Invalid request body',
                examples={
                    'application/json': {
                        'Error': 'Invalid Request Body'
                    }
                }
            ),
            401: openapi.Response(
                description='Unauthorized or invalid connection request',
                examples={
                    'application/json': {
                        'Error': 'Unauthorized or invalid connection'
                    }
                }
            ),
            500: openapi.Response(
                description='Internal server error',
                examples={
                    'application/json': {
                        'Error': 'An unexpected error occurred'
                    }
                }
            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def withdraw_send_request_api_doc(func):
    @swagger_auto_schema(
        method='post',
        operation_description="Withdrawing connection request for the user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'receiver_id': openapi.Schema(type=openapi.TYPE_INTEGER,
                                              description='The receiver_id gives us the receivers user_id '),
            },
            required=['receiver_id']
        ),
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description='Successfully Withdrawn Conncetion Request',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'receiver_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='New refresh token'),

                    }
                ),
                examples={
                    'application/json': {
                        'message': 'Request Withdrawn Successfully',

                    }
                }
            ),
            400: openapi.Response(
                description='Invalid request body',
                examples={
                    'application/json': {
                        'Error': 'Invalid Request Body'
                    }
                }
            ),
            401: openapi.Response(
                description='Unauthorized or invalid withdrawn request',
                examples={
                    'application/json': {
                        'Error': 'Unauthorized or invalid withdraw request'
                    }
                }
            ),
            500: openapi.Response(
                description='Internal server error',
                examples={
                    'application/json': {
                        'Error': 'An unexpected error occurred'
                    }
                }
            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap

def block_user_api_doc(func):
    @swagger_auto_schema(
        method='post',
        operation_description="Blocked user successfully.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'blocked_user_id': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                  description='block user id for block the user'),
            },
            required=['blocked_user_id']
        ),
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description='blocked user using blocked user id',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'blocked_user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='New refresh token'),
                    }
                ),
                examples={
                    'application/json': {
                        'message': 'blocked user successfully',
                    }
                }
            ),
            400: openapi.Response(
                description='Invalid request body',
                examples={
                    'application/json': {
                        'error': 'Invalid Request Body'
                    }
                }
            ),
            404: openapi.Response(
                description='User not found',
                examples={
                    'application/json': {
                        'error': 'User not found'
                    }
                }
            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def list_connection_api_doc(func):
    @swagger_auto_schema(
        method='get',
        operation_description="Retrieve a list of user connections based on the specified connection type",
        manual_parameters=[
            openapi.Parameter(
                'connections_type',
                openapi.IN_QUERY,
                description="Type of connections to retrieve (blocked, accepted, pending)",
                type=openapi.TYPE_STRING,
                required=False
            ),

            openapi.Parameter(
                'friend_id',
                openapi.IN_QUERY,
                description="User ID to retrieve friends of a specific user",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Page number for pagination (default: 1)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'page_size',
                openapi.IN_QUERY,
                description="Number of results per page for pagination (default: 10)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="list connection Token for authorization (e.g., Bearer <token>)",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Connection requests fetched successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'data': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'sender_id': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description='ID of the sender'
                                    ),
                                    'receiver_id': openapi.Schema(
                                        type=openapi.TYPE_INTEGER,
                                        description='ID of the receiver'
                                    ),
                                    'status': openapi.Schema(
                                        type=openapi.TYPE_STRING,
                                        description='Status of the connection'
                                    ),
                                }
                            ),
                            description='List of connection requests'
                        ),
                    },
                    required=['data']
                ),
            ),
            404: openapi.Response(
                description="No connection requests found"
            ),
            400: openapi.Response(
                description="Invalid connection type provided"
            ),
            500: openapi.Response(
                description="Internal server error"
            ),
        },
        security=[{'Bearer': []}]
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def accept_reject_api_doc(func):
    @swagger_auto_schema(
        method='post',
        operation_description="Handle friend request (accept or reject)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'sender_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='The sender_id of the friend request'),
                'action': openapi.Schema(type=openapi.TYPE_STRING, description="Action to perform: 'accept' or 'reject'"),
            },
            required=['sender_id', 'action']
        ),
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description='Successfully handled friend request',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING, description='Request handling status'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description='Detailed message'),
                    }
                ),
                examples={
                    'application/json': {
                        'status': 'success',
                        'message': 'Connection request accepted. You are now connected.',
                    }
                }
            ),
            400: openapi.Response(
                description='Invalid action or request body',
                examples={
                    'application/json': {
                        'error': 'Invalid action',
                    }
                }
            ),
            401: openapi.Response(
                description='Unauthorized request',
                examples={
                    'application/json': {
                        'Error': 'Authorization Token is missing!',
                    }
                }
            ),
            404: openapi.Response(
                description='Connection request not found',
                examples={
                    'application/json': {
                        'error': 'Connection request not found.',
                    }
                }
            ),
            500: openapi.Response(
                description='Internal server error',
                examples={
                    'application/json': {
                        'Error': 'An unexpected error occurred',
                    }
                }
            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def report_user_api_doc(func):
    @swagger_auto_schema(
        method='post',
        operation_description="Report user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'reported_user_id': openapi.Schema(type=openapi.TYPE_INTEGER,
                                                  description='Reported user using their userid'),
                'reason':openapi.Schema(type=openapi.TYPE_STRING,
                                                  description='give some reason for report'),
            },
            required=['reported_user_id','reason']
        ),
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description='Reported user using their user id',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'reported_user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='repoter by using reported user id'),
                        'reason': openapi.Schema(type=openapi.TYPE_STRING, description='reasons for report'),
                    }
                ),
                examples={
                    'application/json': {
                        'message': 'Report user successfully',
                    }
                }
            ),
            400: openapi.Response(
                description='Invalid request body',
                examples={
                    'application/json': {
                        'error': 'Invalid Request Body'
                    }
                }
            ),
            404: openapi.Response(
                description='User not found',
                examples={
                    'application/json': {
                        'error': 'User not found'
                    }
                }
            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def UserWishAddapi_doc(func):
    @swagger_auto_schema(
        method='post',
        operation_description="User Wish created successfully.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING,description='It shows the special events'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='It shows the desire of the user'),
                'tag_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='It show the tag people id'),
            },
            required=['title','description','tag_id']
        ),
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description='User wish created Successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'title': openapi.Schema(type=openapi.TYPE_STRING, description='It shows the special events'),
                        'description': openapi.Schema(type=openapi.TYPE_STRING,description='It shows what he want for this event'),
                        'tag_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='It show the tag people id'),
                    }
                ),
                examples={
                    'application/json': {
                        'message': 'User wish created succesfully',
                    }
                }
            ),
            400: openapi.Response(
                description='Invalid request body',
                examples={
                    'application/json': {
                        'error': 'Invalid Request Body'
                    }
                }
            ),
            404: openapi.Response(
                description='User not found',
                examples={
                    'application/json': {
                        'error': 'User not found'
                    }
                }
            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap



def get_user_wish_api_doc(func):
    @swagger_auto_schema(
        method='get',
        operation_description="User Wish get profile",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Page number for pagination (default: 1)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'page_size',
                openapi.IN_QUERY,
                description="Number of results per page for pagination (default: 10)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
        ],

        responses={
            200: openapi.Response(
                description='User Wish profile',
                examples={
                    'application/json': {
                        'Success': 'User Wish Profile '
                    }
                }
            ),
            400: openapi.Response(
                description='Invalid request body',
                examples={
                    'application/json': {
                        'Error': 'Invalid request body'
                    }
                }
            )
        }
    )
    @ wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)
    return wrap


def user_wish_update_api_doc(func):
    @swagger_auto_schema(
        method='put',
        operation_description="User Wish Updated successfully.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='It shows the special events'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='It shows the desire of the user'),
            },
            required=['title', 'description']
        ),
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description='User wish updated Successfully',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'title': openapi.Schema(type=openapi.TYPE_STRING, description='It shows the title of the user_wish '),
                        'description': openapi.Schema(type=openapi.TYPE_STRING,description='It shows what he needs in this wish'),
                    }
                ),
                examples={
                    'application/json': {
                        'message': 'User wish Updated succesfully',
                    }
                }
            ),
            400: openapi.Response(
                description='Invalid request body',
                examples={
                    'application/json': {
                        'error': 'Invalid Request Body'
                    }
                }
            ),
            404: openapi.Response(
                description='User not found',
                examples={
                    'application/json': {
                        'error': 'User not found'
                    }
                }
            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap

def search_username_api_doc(func):
    @swagger_auto_schema(
        method='get',
        operation_description="Search Username in Logged ID ",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Page number for pagination (default: 1)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'page_size',
                openapi.IN_QUERY,
                description="Number of results per page for pagination (default: 10)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'username',
                openapi.IN_QUERY,
                description="Partial or full username to search for. The API returns users whose usernames contain this value.",
                type=openapi.TYPE_STRING,
                required=False,
            ),
    ],


        responses={
            200: openapi.Response(
                description="A list of users matching the search criteria",
                schema=LoginSerializer(many=True)
            ),
            500: openapi.Response(
                description="Internal server error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap

def get_profile_view_api_doc(func):
    @swagger_auto_schema(
        method='get',
        operation_description="Get friend's profile view",
        manual_parameters=[
            openapi.Parameter(
                'Authorization',
                openapi.IN_HEADER,
                description="Bearer token",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                'connection_id',
                openapi.IN_QUERY,
                description="ID of the connection (friend)",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Page number for pagination (default: 1)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'page_size',
                openapi.IN_QUERY,
                description="Number of results per page for pagination (default: 10)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
        ],
        responses={
            200: openapi.Response(
                description='Friend\'s profile retrieved successfully',
                examples={
                    'application/json': {
                        'data': {
                        }
                    }
                }
            ),
            400: openapi.Response(
                description='User Not Found',
                examples={
                    'application/json': {
                        'error': 'User Not Found'
                    }
                }
            ),
            403: openapi.Response(
                description='You are not friends with this user',
                examples={
                    'application/json': {
                        'error': 'You are not friends with this user'
                    }
                }
            ),
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


def reset_api_doc(func):
    @swagger_auto_schema(
        method='post',
        operation_description="Reset password",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username or email'),
                'old_password': openapi.Schema(type=openapi.TYPE_STRING, description='Old password'),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='New password')
            },
            required=['username',  'old_password', 'new_password']
        ),
        responses={
            200: openapi.Response(
                description='Password reset successfully',
                examples={
                    'application/json': {
                        'success': True,
                        'message': 'Password reset successfully'
                    }
                }
            ),
            400: openapi.Response(
                description='Invalid data',
                examples={
                    'application/json': {
                        'success': False,
                        'message': 'Invalid data'
                    }
                }
            ),
            404: openapi.Response(
                description='User or security question not found',
                examples={
                    'application/json': {
                        'error': 'User not found or security question not found'
                    }
                }
            ),
            401: openapi.Response(
                description='Incorrect security question or answer',
                examples={
                    'application/json': {
                        'error': 'Security question or answer is incorrect'
                    }
                }
            )
        }
    )
    @wraps(func)
    def wrap(request, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrap


