from django.contrib import admin
from .models import UserConnection,BlockedUser,ReportedUser

# Register your models here.
admin.site.register(UserConnection)
admin.site.register(BlockedUser)
admin.site.register(ReportedUser)

