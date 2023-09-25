from django.core.mail import send_mail
from decouple import config


def send_activation_code(email, code):
    send_mail(
        'Melonm API',
        f'Привет! Ссылка для активации аккаунта: \n\n http://{config("HOST", default="127.0.0.1")}:{config("PORT", default="8000")}/api/v1/account/activate/{code}',
        'py29.hakaton@gmail.com',
        [email]
    )


def send_code_forgot_password(email, code):
    send_mail(
        'Melorm API',
        f'Код для восстановления вашего пароля: {code} ',
        'py29.hakaton@gmail.com',
        [email]
    )
