from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenBlacklistSerializer

from accounts.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields= ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # Accept either username or email through a single "user" field.
    user = serializers.CharField()

    def __init__(self, *args, **kwargs):
        # Initialize the parent serializer and its default fields.
        super().__init__(*args, **kwargs)
        # Remove the default email required input field 
        # because the client will provide username or email through the "user" field.
        self.fields.pop('email', None)

    def validate(self, attrs):
        # Get the user input(username or email) and password from the request data(attrs).
        user = attrs.get('user')

        # Find the account using email or username.
        if '@' in user:
            account_user = User.objects.filter(email=user).first()
        else:
            account_user = User.objects.filter(username=user).first()

        # Raise an authentication error if the account does not exist
        if account_user is None:
            raise AuthenticationFailed('Invalid username or email')

        # Add the account's actual email from account_user.email
        # because the parent serializer uses the User model's USERNAME_FIELD (email) for authentication.
        attrs['email'] = account_user.email

        # Let SimpleJWT authenticate the user and generate access and refresh tokens.
        validate_data = super().validate(attrs)

        # Add the authenticated user's information to the response data.
        validate_data['user'] = {
            'username': account_user.username,
            'email': account_user.email
        }

        return validate_data

    default_error_messages = {
        'no_active_account': 'Invalid password'
    }

class LogoutSerializer(TokenBlacklistSerializer):
    pass

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user

        if not user.check_password(value):
            raise serializers.ValidationError("Invalid Old Password")

        return value

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        if new_password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")
        
        return attrs

    def update(self, instance, validated_data):
        new_password = validated_data.get('new_password')

        if new_password:
            instance.set_password(new_password)
            instance.save()

        return instance

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        user = User.objects.filter(email=value).first()

        if user is None:
            raise serializers.ValidationError("User with this email doesn't exist")

        return value

    def save(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        print("User PK:", user.pk)
        print("Encoded UID:", uid)

        reset_link = f"http://localhost:3000/reset-password/{uid}/{token}"

        send_mail(
            subject="Reset Your Password",
            message=f"Click the link below to reset your password: {reset_link}",
            from_email='blogapi@gmail.com',
            recipient_list=[email]
        )

class PasswordResetSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        uid = attrs.get('uid')
        token = attrs.get('token')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (User.DoesNotExist, ValueError, TypeError):
            raise serializers.ValidationError("Invalid user ID")

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError("Invalid or expired token")

        if new_password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")

        try:
            validate_password(new_password, user)
        except ValidationError as error:
            raise serializers.ValidationError({
                'new_password': list(error.messages)
            })

        attrs['user'] = user
        return attrs

    def update(self, instance, validated_data):
        new_password = validated_data.get('new_password')

        instance.set_password(new_password)
        instance.save()

        return instance