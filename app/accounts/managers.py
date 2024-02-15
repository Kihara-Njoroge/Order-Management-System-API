from datetime import timedelta
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class MyUserManager(BaseUserManager):

    def _create_user(
        self, email, phone, user_name, first_name, last_name, password, **extra_fields
    ):
        """Creates a new user with the given information.
        Parameters:
            - email (str): User's email address.
            - phone (str): User's phone number.
            - user_name (str): User's desired username.
            - first_name (str): User's first name.
            - last_name (str): User's last name.
            - password (str): User's desired password.
            - **extra_fields (dict): Additional fields to be included in the user's information.
        Returns:
            - user (User): Newly created user object.
        Processing Logic:
            - Validates that all required fields are provided.
            - Normalizes the email address.
            - Sets the user's password.
            - Saves the user to the database."""
        if not email:
            raise ValueError(_("Email field is required"))
        if not phone:
            raise ValueError(_("Phone field is required"))
        if not user_name:
            raise ValueError(_("Username is required"))
        if not first_name:
            raise ValueError(_("First name is required"))
        if not last_name:
            raise ValueError(_("Last name is required"))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            phone=phone,
            user_name=user_name,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self,
        email,
        phone,
        user_name,
        first_name=None,
        last_name=None,
        password=None,
        **extra_fields
    ):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(
            email, phone, user_name, first_name, last_name, password, **extra_fields
        )
        
    def create_superuser(
        self,
        email,
        phone,
        user_name,
        first_name=None,
        last_name=None,
        password=None,
        **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self._create_user(
            email, phone, user_name, first_name, last_name, password, **extra_fields
        )
        
    def set_otp(self, user, otp):
        user.otp = otp
        user.otp_expiration = timezone.now() + timedelta(minutes=10)
        user.save()

    def verify_otp(self, user, otp):
        if user.otp == otp and user.otp_expiration >= timezone.now():
            user.is_verified =True
            user.otp = None
            user.otp_expiration = None
            user.save()
            return True
        return False
