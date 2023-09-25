from django.urls import path
from applications.order.views import OrderAPIView, MyHistoryAPIView, HistoryAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', OrderAPIView)

urlpatterns = [
    path('my-history/', MyHistoryAPIView.as_view()),
    path('history/', HistoryAPIView.as_view())
]

urlpatterns+=router.urls
