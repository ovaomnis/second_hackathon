from rest_framework.routers import DefaultRouter
from applications.feedback.views import *

router = DefaultRouter()
router.register('comment', CommentModelViewSet)

urlpatterns = []

urlpatterns += router.urls