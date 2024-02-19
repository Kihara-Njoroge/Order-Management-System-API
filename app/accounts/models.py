from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import Group
from .managers import MyUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid


# Create your models here
class CustomUser(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(verbose_name=_("Username"), max_length=255, unique=True)
    phone_number = models.CharField(_("Phone Number"), unique=True, max_length=15)
    email = models.EmailField(_("Email Address"), max_length=254, unique=True)
    first_name = models.CharField(
        _("First Name"),
        max_length=254,
        help_text=_("The first name as it appears on ID or passport"),
    )
    last_name = models.CharField(
        _("Last Name"),
        max_length=254,
        help_text=_("The first name as it appears on ID or passport"),
    )

    is_staff = models.BooleanField(
        _("Staff Status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_("Designates whether this user should be treated as active."),
    )
    is_verified = models.BooleanField(
        _("User Verified"),
        default=False,
        help_text=_("Designates whether the user is a verified user"),
    )
    date_joined = models.DateTimeField(_("Date Joined"), default=timezone.now)
    otp = models.PositiveIntegerField(null=True, blank=True)
    otp_expiration = models.DateTimeField(null=True, blank=True)
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name=_("user permissions"),
        blank=True,
        related_name="custom_user_permissions",
        help_text=_("Specific permissions for this user."),
        related_query_name="user",
    )
    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        related_name="custom_user_groups",
        related_query_name="user",
    )

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone_number", "username"]

    class Meta:
        app_label = "accounts"
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-date_joined"]

    def __str__(self):
        return self.username

    def get_full_name(self):
        """
        Returns the first_name plus the last_name
        """
        first_name = self.first_name.strip()
        last_name = self.last_name.strip()
        full_name = f"{first_name} {last_name}"
        return full_name
