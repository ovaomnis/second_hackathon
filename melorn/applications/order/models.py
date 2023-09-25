import random
import uuid

from django.db import models
from django.contrib.auth import get_user_model
from applications.product.models import Product

User = get_user_model()


class Order(models.Model):
    """
    Модель для информации о заказе
    """

    STATUS = (
        ('ORDER_PROCESSING', 'Обработка заказа'),
        ('SUCCESSFULLY', 'Успешно ожидайте заказ в течение недели'),
        ('ARRIVED', 'Ваш заказ прибыл!'),
        ('RECEIVED', 'Получен')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_status = models.CharField('Статус заказа', choices=STATUS, default=STATUS[0][0], max_length=16)
    order_comment = models.TextField(blank=True, null=True)
    order_create_at = models.DateTimeField(auto_now_add=True)

    signer_email = models.EmailField(null=True, blank=True)
    signer_firstname = models.CharField('Имя заказчика', max_length=50)
    signer_lastname = models.CharField('Фамилия заказчика', max_length=50)
    signer_address = models.CharField('Адрес доставки', max_length=1000)
    signer_phone = models.CharField('Контактный телефон', max_length=11)

    order_id = models.CharField('ID заказа', max_length=6, unique=True, default='')

    def save(self, *args, **kwargs):
        if not self.order_id:
            order_id = uuid.uuid4().hex[:6]
            while Order.objects.filter(order_id=order_id).exists():
                order_id = uuid.uuid4().hex[:6]
            self.order_id = order_id
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Заказ ID:{self.order_id}'


class OrderItem(models.Model):
    """
        Модель товара в заказе
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_items')
    amount = models.PositiveIntegerField('Количество', default=1)

    def __str__(self):
        return f"{self.product} x{self.amount}"
