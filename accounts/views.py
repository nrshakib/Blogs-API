from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.serializers import CustomTokenObtainPairSerializer, UserRegistrationSerializer

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