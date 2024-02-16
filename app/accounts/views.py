from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import update_last_login
from django.utils import timezone
from datetime import timedelta
import random
from .serializers import CustomUserSerializer
from .models import CustomUser
from .responses import UserResponses

u_responses = UserResponses()

class UserViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    
    def create_user(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            if CustomUser.objects.filter(email=serializer.validated_data['email']).exists():
                return Response(u_responses.user_exists_error(serializer.data), status=status.HTTP_400_BAD_REQUEST)
            else:
                user = serializer.save()
                return Response(u_responses.user_created_success(serializer.data), status=status.HTTP_201_CREATED)
        return Response(u_responses.create_user_error(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['put'])
    def update_user(self, request, pk=None):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(u_responses.user_update_success(serializer.data))
        return Response(u_responses.user_update_error(), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['delete'])
    def delete_user(self, request, pk=None):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # perform delete action here

        return Response(u_responses.delete_user_success(serializer.data))

    @action(detail=False, methods=['get'])
    def get_user(self, request, pk=None):
        try:
            user = CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CustomUserSerializer(user)
        return Response(u_responses.get_user_success(serializer.data))