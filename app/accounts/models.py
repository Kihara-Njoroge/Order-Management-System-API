from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import MyUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(verbose_name=_(
        "Username"), max_length=255, unique=True)
    phone = models.CharField(_("phone number"), unique=True, max_length=15)
    email = models.EmailField(_("email address"), max_length=254, unique=True)
    first_name = models.CharField(
        _("first name"),
        max_length=254,
        help_text=_("The first name as it appears on ID or passport"),
    )
    last_name = models.CharField(
        _("last name"),
        max_length=254,
        help_text=_("The first name as it appears on ID or passport"),
    )
    user_name = models.CharField(
        _("username"), max_length=254, help_text=_("unique app identifier"), unique=True
    )

    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as"
        ),
    )
    is_verified = models.BooleanField(
        _("user verified"),
        default=False,
        help_text=_("Designates whether the user is a verified user"),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    otp = models.PositiveIntegerField(null=True, blank=True)
    otp_expiration = models.DateTimeField(null=True, blank=True)

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone", "username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
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
