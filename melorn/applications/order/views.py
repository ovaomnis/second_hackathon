from urllib.request import Request

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import Order
from applications.order.serializers import OrderSerializer
from rest_framework.response import Response

User = get_user_model()


class OrderAPIView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == ['list', 'update', 'delete']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MyHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        queryset = Order.objects.filter(user=request.user, order_status=Order.STATUS[3][0])
        sz = OrderSerializer(instance=queryset, many=True)
        return Response(sz.data)

class HistoryAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        email = request.GET.get('email', None)

        if email:
            queryset = Order.objects.filter(user__email=email, order_status=Order.STATUS[3][0])
        else:
            queryset = Order.objects.filter(order_status=Order.STATUS[3][0])
        sz = OrderSerializer(instance=queryset, many=True)
        return Response(sz.data)
