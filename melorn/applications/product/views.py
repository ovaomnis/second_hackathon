from rest_framework import viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from core.permissions import IsAdminOrReadOnly

from .models import (Category,
                     SpecName,
                     Spec,
                     Product)
from .serializers import (CategoryListSerializer,
                          CategoryDetailSerializer,
                          SpecNameSerializer,
                          SpecSerializer,
                          ProductDetailSerializer,
                          ProductListSerializer)

from applications.feedback.models import (Like,
                                          Rating)
from applications.feedback.serializers import (RatingSerializer)


# Create your views here.
class CategoryAPIView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        if self.action == 'list':
            self.queryset = Category.objects.filter(parent=None)
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == 'list':
            self.serializer_class = CategoryListSerializer
        return super().get_serializer_class()


class SpecNameAPIView(viewsets.ModelViewSet):
    queryset = SpecName.objects.all()
    serializer_class = SpecNameSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['name']
    ordering_fields = ['name']
    search_fields = ['name', 'cat__name']

    def get_queryset(self):
        cat_slug = self.request.query_params.get('cat')
        queryset = super().get_queryset()
        if cat_slug:
            cat = get_object_or_404(Category, slug=cat_slug)
            queryset = queryset.filter(cat__in=cat.get_descendants(include_self=True))
        return self.filter_queryset(queryset)


class SpecAPIView(viewsets.ModelViewSet):
    queryset = Spec.objects.all()
    serializer_class = SpecSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['name']
    search_fields = ['value', 'name__name', 'name__cat__name']
    ordering_fields = ['value', 'name']


class ProductAPIView(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ['cat']
    search_fields = ['slug', 'name', 'description', 'cat__name']
    ordering_fields = ['created']

    # Actions
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        product = self.get_object()
        sz = self.get_serializer(product)
        product.views += 1
        product.save()
        return Response(sz.data, status=200)

    @action(detail=True, methods=['GET'])
    def like(self, request: Request, *args, **kwargs) -> Response:
        product = self.get_object()
        like, _ = Like.objects.get_or_create(owner=request.user, product=product)
        like.is_like = not like.is_like
        like.save(update_fields=('is_like',))
        if like.is_like:
            return Response('like')
        return Response('unlike')

    @action(detail=True, methods=['POST'])
    def rating(self, request: Request, *args, **kwargs) -> Response:
        product = self.get_object()
        rating, _ = Rating.objects.get_or_create(owner=self.request.user, product=product)
        sz = RatingSerializer(instance=rating, data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(sz.data)

    # Getters
    def get_queryset(self):
        specs = self.request.query_params.get('specs')
        queryset = super().get_queryset()
        if specs:
            queryset = queryset.filter(specs__in=specs.split(','))

        return self.filter_queryset(queryset.distinct())

    def get_serializer_class(self):
        if self.action == 'list':
            self.serializer_class = ProductListSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ('like', 'rating'):
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()
