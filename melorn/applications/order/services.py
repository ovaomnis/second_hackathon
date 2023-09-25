from django.core.mail import send_mail


def send_order_confirmed(email, order_number):
    send_mail(
        'Melorm API',
        f'Ваш заказ №{order_number} был успешно обработан и отправлен в отсортировочный центр',
        'py29.hakaton@gmail.com',
        [email]
    )
