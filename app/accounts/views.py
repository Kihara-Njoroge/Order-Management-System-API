from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import CustomUserSerializer, UpdateCustomUserSerializer, ReadCustomUserSerializer, UserLoginSerializer
from .models import CustomUser
from .responses import UserResponses
from django.contrib.auth import authenticate, get_user_model, login, logout
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt



u_responses = UserResponses()


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_serializer_class(self):
        """
        Return the serializer class to use for the current request.
        """
        if self.action == "create":
            return CustomUserSerializer
        elif self.action == "retrieve":
            return ReadCustomUserSerializer
        elif self.action in ["update", "partial_update"]:
            return UpdateCustomUserSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if CustomUser.objects.filter(email=serializer.validated_data['email']).exists():
            return Response(u_responses.user_exists_error(serializer.data), status=status.HTTP_400_BAD_REQUEST)
        else:
            self.perform_create(serializer)
            return Response(u_responses.user_created_success(serializer.data), status=status.HTTP_201_CREATED)


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(u_responses.get_user_success(serializer.data))

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(u_responses.get_user_success(serializer.data))

    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(u_responses.user_update_success(serializer.data))
    def destroy(self, request, pk=None):
        try:
            user = CustomUser.objects.get(pk=pk)
            user.delete()
            return Response(u_responses.delete_user_success(pk))
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)




class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer


    @csrf_exempt
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, email=email, password=password)
        if user is None or not user.is_active:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        response = Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)
        response.set_cookie('refresh', str(refresh), httponly=True, secure=True)

        return response


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()

        logout(request)

        response = Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)

        response.delete_cookie('token')

        return response