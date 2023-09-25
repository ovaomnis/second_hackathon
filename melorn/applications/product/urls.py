from rest_framework.routers import DefaultRouter

from .views import CategoryAPIView, SpecNameAPIView, SpecAPIView, ProductAPIView

router = DefaultRouter()
router.register('category', CategoryAPIView)
router.register('spec-name', SpecNameAPIView)
router.register('spec', SpecAPIView)
router.register('', ProductAPIView)

urlpatterns = router.urls
