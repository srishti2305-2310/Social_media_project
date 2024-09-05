from datetime import datetime, timedelta
from functools import wraps


import jwt
from django.conf import settings
from django.http import JsonResponse
from rest_framework import status

from User_Auth.models import User

# Secret key for signing the JWT
SECRET_KEY = settings.SECRET_KEY

# Token expiration time
ACCESS_TOKEN_LIFETIME = timedelta(minutes=45)
REFRESH_TOKEN_LIFETIME = timedelta(days=1)


def generate_access_token(user):
    """
    Generate an access token for a user.

    Args:
        user (User): The user object for which the token is generated.

    Returns:
        str: The encoded JWT access token.
    """
    expiration = datetime.utcnow() + ACCESS_TOKEN_LIFETIME
    payload = {
        'user_id': user.id,
        'exp': expiration,
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def generate_refresh_token(user):
    """
    Generate a refresh token for a user.

    Args:
        user (User): The user object for which the token is generated.

    Returns:
        str: The encoded JWT refresh token.
    """
    expiration = datetime.utcnow() + REFRESH_TOKEN_LIFETIME
    payload = {
        'user_id': user.id,
        'exp': expiration,
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def decode_token(token):
    """
    Decode a JWT token.

    Args:
        token (str): The JWT token to decode.

    Returns:
        dict: The decoded payload if the token is valid.
        JsonResponse: An error response if the token is expired or invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return JsonResponse({"message": "Token is expired"}, status=status.HTTP_498_INVALID_TOKEN)
    except jwt.InvalidTokenError:
        return JsonResponse({"message": "Invalid token"}, status=status.HTTP_403_FORBIDDEN)


def is_auth(fun):
    """
    Decorator to check if the request is authenticated.

    Args:
        fun (function): The view function to wrap.

    Returns:
        function: The wrapped function that checks for authentication.
    """

    @wraps(fun)
    def wrap(request, *args, **kwargs):
        """
        Wrapper function to check for JWT token in the request headers.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The response from the wrapped function or an error response.
        """

        try:
            token = request.headers.get('Authorization')

            if not token:
                return JsonResponse({"message": "Authorization Token is missing!"}, status=status.HTTP_403_FORBIDDEN)

            decode_token_result = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])  # (token)

            request.decoded_token_result = decode_token_result
            request.user_id = request.decoded_token_result.get("user_id")
            user = User.objects.get(id=request.user_id)
            if user.is_block:
                return JsonResponse({"message": "User is blocked"}, status=status.HTTP_403_FORBIDDEN)

            return fun(request, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"message": "Token is expired"}, status=status.HTTP_403_FORBIDDEN)
        except jwt.InvalidTokenError:
            return JsonResponse({"message": "Invalid token"}, status=status.HTTP_403_FORBIDDEN)

    return wrap
