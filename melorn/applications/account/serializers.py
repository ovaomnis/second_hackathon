from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.shortcuts import get_object_or_404
from applications.account.services import send_code_forgot_password

# from applications.account.services import send_activation_code
from applications.account.tasks import celery_send_activation_code

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password_again = serializers.CharField(required=True, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_again')

    def validate_email(self, email):
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.pop('password_again')

        if password != password2:
            raise serializers.ValidationError('Первый и Второй пароли не совпадают!')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        celery_send_activation_code.delay(user.email, user.code)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def send_code(self):
        user = get_object_or_404(User, email=self.validated_data.get('email'))
        user.create_activation_code()
        send_code_forgot_password(user.email, user.code)


class ForgotPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)

    def validate(self, attrs):
        email = attrs.get('email')
        code = attrs.get('code')
        user = get_object_or_404(User, email=email, code=code)
        attrs['user'] = user
        return attrs

    def set_new_password(self):
        password = self.validated_data.get('new_password')
        user = self.validated_data.get('user')
        user.set_password(password)
        user.save()


