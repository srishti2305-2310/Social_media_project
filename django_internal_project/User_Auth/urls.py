from django.urls import path

from .views import forgot_password_api, update_security_q_a, get_security_q_a, reset_password_api
from .views import get_profile, user_delete
from .views import user_login, signup_api, update_profile, user_logout, get_refresh_token, send_test_email

urlpatterns = [
    path('signup/', signup_api, name='signup'),
    path('login/', user_login, name='login'),
    path('forgot-password/', forgot_password_api, name='forgot-password'),
    path('update-security-q/', update_security_q_a, name='update-security-q'),
    path('get-question/', get_security_q_a, name='get-question'),

    path('update-profile/', update_profile, name='update-profile'),
    path('logout/', user_logout, name='logout'),

    path('profile/', get_profile, name='profile'),
    path('delete/', user_delete, name='delete'),


    path('refresh-token/', get_refresh_token, name='refresh-token'),
    path('send-email/', send_test_email, name='send_test_email'),

    path('reset-password/',reset_password_api,name='reset-password')


]
