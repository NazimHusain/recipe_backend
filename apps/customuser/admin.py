
from django.contrib import admin
from apps.customuser import models as User


class AdminUser(admin.ModelAdmin):
    list_display = ("id","email", "username","role","profilePic")
admin.site.register(User.User, AdminUser)

