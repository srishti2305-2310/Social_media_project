from django.contrib import admin

from User_Auth.models import User, UsersecurityQuestion
from utility.email_utils import send_email


# Define the custom action
def block_users(modeladmin, request, queryset):
    queryset.update(is_block=True)
    for user in queryset:
        subject = "Your Account Has Been Blocked"
        plain_text_body = f"Hi {user.username}, your account has been blocked due to policy violations."
        html_template_path = "account_blocked_email.html"  # Ensure this template exists
        context = {
            "username": user.username,
            "support_link": "https://example.com/support"  # Replace with actual link
        }
        to_email = user.email

        send_email(subject, plain_text_body, html_template_path, context, to_email)
    modeladmin.message_user(request, "Selected users have been blocked.")


block_users.short_description = "Block selected users"


def unblock_users(modeladmin, request, queryset):
    queryset.update(is_block=False)
    modeladmin.message_user(request, "Selected users have been unblocked.")


unblock_users.short_description = "Unblock selected users"


# Register your User model with the custom action
class UserAdmin(admin.ModelAdmin):
    actions = [block_users, unblock_users]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_block')
    list_filter = ('is_block',)
    search_fields = ('username', 'email', 'first_name', 'last_name')


admin.site.register(User, UserAdmin)
admin.site.register(UsersecurityQuestion)
