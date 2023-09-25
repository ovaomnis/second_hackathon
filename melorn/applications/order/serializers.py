from rest_framework import serializers
from applications.order.models import Order
from django.contrib.auth import get_user_model
from applications.order.services import send_order_confirmed

from .models import OrderItem

User = get_user_model()


class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.ReadOnlyField(source='order.order_id')
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    order_items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        order_items = validated_data.pop('order_items')

        instance = super().create(validated_data)
        OrderItem.objects.bulk_create([OrderItem(order=instance, **order_item) for order_item in order_items])

        send_order_confirmed(instance.user.email, instance.order_id)
        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.update({
            "order_status": dict(instance.STATUS).get(instance.order_status)
        })
        return rep
