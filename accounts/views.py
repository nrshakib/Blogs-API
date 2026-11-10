from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView

from accounts.serializers import CustomTokenObtainPairSerializer, LogoutSerializer, PasswordChangeSerializer, UserRegistrationSerializer

class UserRegistrationView(GenericAPIView, CreateModelMixin):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)

        return Response({
            "message": "User Created Successfully",
            "status_text": 'success',
            "data": response.data
        }, status=status.HTTP_201_CREATED)

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        return Response({
            'message': 'Login Successful',
            'status_text': 'success',
            'data': response.data['user'],
            'tokens': {
                'access': response.data['access'],
                'refresh': response.data['refresh']
            }
        }, status=response.status_code)

class LogoutView(TokenBlacklistView):
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        return Response({
            "message": "User Logged out Successfully",
            "status_text": "success",
        }, status=response.status_code)

class ChangePasswordView(GenericAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data = request.data,
            instance = request.user
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Password Updated Successfully",
            "status_text": "success"
        }, status=status.HTTP_200_OK)
