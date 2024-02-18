from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


# Register your models here.
class CustomUserAdmin(BaseUserAdmin):
    ordering = ['-date_joined']
    model = CustomUser
    list_display = [
        'id',
        'email',
        'username',
        'first_name',
        'last_name',
        'phone_number',
        'is_staff',
        'is_active',
        'is_verified'
    ]
    list_display_links = ['id', 'email']
    list_filter = ['email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active']

    fieldsets = (
        (
            _("Login Credentials"),
            {
                "fields": (
                    "email",
                    "password",
                    "otp",
                )
            },
        ),
        (
            _("Personal Information"),
            {
                "fields": (
                    "username",
                    "first_name",
                    "last_name",
                    "phone_number",
                )
            },
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )
    search_fields = ["email", "username", "first_name", "last_name"]


admin.site.register(CustomUser, CustomUserAdmin)