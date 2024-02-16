from rest_framework import serializers
from .models import CustomUser
from .responses import UserResponses


class CustomUserSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(
        label="Repeat Password",
        write_only=True,
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "user_name",
            "first_name",
            "last_name",
            "phone",
            "password",
            "re_password",
        ]
        read_only_fields = ("is_active", "is_staff", "is_verified")
        extra_kwargs = {
            "password": {"write_only": True},
            "error_messages": {
                "required": "The {field_name} field is required",
                "blank": "The {field_name} field cannot be blank",
            },
            "last_name": {
                "error_messages": {"required": "The last name field is required"}
            },
            "first_name": {
                "error_messages": {"required": "The first name field is required"}
            },
            "email": {"error_messages": {"required": "The email field is required"}},
            "phone": {"error_messages": {"required": "The phone field is required"}},
        }

    def validate(self, data):
        if data["password"] != data.pop("re_password"):
            raise serializers.ValidationError(
                UserResponses.password_mismatch_error(), code="Password Mismatch"
            )
        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = uCustomUser.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UpdateCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "phone"]


class DeleteUserSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)


class EnableUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True, error_messages={"required": "The email field is required"}
    )


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    re_password = serializers.CharField(required=True)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True,
        max_length=254,
        error_messages={"required": "The old password field is required"},
    )
    password = serializers.CharField(
        required=True,
        max_length=254,
        error_messages={"required": "The new password field is required"},
    )
    re_password = serializers.CharField(
        required=True,
        max_length=254,
        error_messages={"required": "The re password field is required"},
    )


class ReadCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "user_name",
            "is_staff",
            "date_joined",
        ]
        read_only_fields = ("is_active", "is_staff", "is_verified")


class RegisterUserResponseSerializer(serializers.Serializer):
    access = serializers.CharField()


class VerifyOTPSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    otp = serializers.IntegerField()


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
