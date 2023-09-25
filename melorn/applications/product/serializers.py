from rest_framework import serializers
from django.db.models import Avg
from django.utils.text import slugify

from .models import Category, SpecName, Spec, Product, ProductImage
from ..feedback.serializers import LikeSerializer, CommentSerializer


class CategoryListSerializer(serializers.ModelSerializer):
    childs = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('name', 'slug', 'parent', 'childs',)

    def get_childs(self, obj):
        return CategoryListSerializer(obj.get_children(), many=True).data


class CategoryDetailSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ('name', 'slug', 'parent', 'recommend')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.update({
            'filters': SpecNameSerializer(SpecName.objects.filter(cat__in=instance.get_descendants(include_self=True)), many=True).data
        })
        return rep


class SpecSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Spec
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.update({
            'name': instance.name.name
        })
        return rep

    def create(self, validated_data):
        
        instance = self.Meta.model.objects.filter(slug=slugify(f'{validated_data.get("name")} {validated_data.get("value")}', allow_unicode=True))
        if instance:
            return instance[0]
        return super().create(validated_data)


class SpecNameSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    values = SpecSerializer(many=True, read_only=True)

    class Meta:
        model = SpecName
        fields = "__all__"

    def create(self, validated_data):
        instance = self.Meta.model.objects.filter(slug=slugify(validated_data.get('name'), allow_unicode=True), cat=validated_data.get('cat'))
        if instance:
            return instance[0]
        return super().create(validated_data)


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductListSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = ('name', 'price', 'slug', 'available', 'images', 'likes')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.update({
            'rating': instance.ratings.aggregate(avg_rating=Avg('rating'))['avg_rating'],
            'likes': instance.likes.filter(is_like=True).count()
        })
        return rep


class ProductDetailSerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        exclude = ('created_at', 'updated_at')
        extra_kwargs = {
            'specs': {'required': False}
        }

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep.update({
            'specs': SpecSerializer(instance.specs.all(), many=True).data,
            'rating': instance.ratings.aggregate(avg_rating=Avg('rating'))['avg_rating'],
            'likes': instance.likes.filter(is_like=True).count(),
            'recommendations': ProductListSerializer(self.Meta.model.objects.filter(cat__in=instance.cat.recommend.all())[:10], many=True).data
        })
        return rep

    def create(self, validated_data):
        images = self.context.get('request').FILES.getlist('images')
        product = super().create(validated_data)

        if not images:
            raise serializers.ValidationError({'images': 'Хотя бы одна фотография должна быть загружена'})

        ProductImage.objects.bulk_create([ProductImage(product=product, image=image) for image in images])

        return product
