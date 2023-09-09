from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from common.admin_utils import FieldSets
from users.models import Email, User

# Register your models here.


class EmailAdmin(admin.ModelAdmin):
    list_display = ("email", "user", "verified_at", "is_primary")
    list_filter = ("user", "is_primary")


class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "last_login", "is_active")
    list_filter = ("is_active", "is_staff")
    search_fields = ("username", "email", "phone_number")
    filter_horizontal = []

    fieldsets = FieldSets(
        none=("username", "password"),
        personal_info=("email", "phone_number"),  # , "avatar"),
        permissions=("is_active", "is_staff", "is_superuser"),
        important_dates=("last_login",),
    )

    readonly_fields = ("created",)


# admin.site.register(Email, EmailAdmin)
admin.site.register(User, UserAdmin)
