import json
import random
from datetime import timedelta

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CreateUserSerializer, UserLoginSerializer

User = get_user_model()


class UserViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def user_signup(self, request):
        if request.method == 'POST':
            serializer = CreateUserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()

                user.save()


                return Response(
                    {
                        "message": "User registered successfully.",
                        "user": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# authenticate user
class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # Authenticate the user
            user = authenticate(request, email=email, password=password)

            if user is not None and user.is_active:  # Check if the user is active
                # Delete the existing token (if any)
                Token.objects.filter(user=user).delete()

                login(request, user)

                # Create a new token with an expiration time
                token, created = Token.objects.get_or_create(user=user)
                token.expires = timezone.now() + timedelta(hours=24)  # Set expiration time
                token.save()

                response = Response({'token': token.key}, status=status.HTTP_200_OK)
                response.set_cookie(key='token', value=token.key, httponly=True)

                return response
            elif user is not None:
                return Response(
                    {'error': 'User is not active'}, status=status.HTTP_401_UNAUTHORIZED
                )
            else:
                return Response(
                    {'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Delete the existing token and related cookies
        user = request.user
        Token.objects.filter(user=user).delete()

        # Logout the user
        logout(request)

        response = Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

        # Delete the token cookie
        response.delete_cookie('token')

        return response
