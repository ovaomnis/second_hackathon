from rest_framework.authtoken.models import Token
import random
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from applications.account.serializers import RegisterSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, ForgotPasswordResetSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User


from applications.account.services import send_code_forgot_password

User = get_user_model()

class RegisterAPIView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response('Регистрация прошла успешно! Код активации был отправлен вам на почту', status=201)


class ActivationAPIView(APIView):
    def get(self, request, code):
        user = get_object_or_404(User, code=code)
        user.is_active = True
        user.code = ''
        user.save(update_fields=('is_active', 'code'))
        return Response('Регистрация прошла успешно!', status=200)


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')


            if not user.check_password(old_password):
                return Response('Старый пароль неверен', status=400)
            user.set_password(new_password)
            user.save()

            return Response('Пароль успешно изменен', status=200)

        return Response(serializer.errors, status=400)


class ForgotPasswordAPIView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_code()
        return Response('Код активации был отравлен на вашу почту')


class ForgotPasswordResetAPIView(APIView):
    def post(self, reqeust):
        serializer = ForgotPasswordResetSerializer(data=reqeust.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Пароль был успешно изменен')
