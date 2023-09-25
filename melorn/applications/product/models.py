from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from core.utils import generate_unique_slug
from core.models import CreatedUpdatedModelMixin


# Create your models here.
class Category(MPTTModel):
    slug = models.SlugField(primary_key=True)
    name = models.CharField(max_length=127)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, related_name='childs', null=True, blank=True)
    recommend = models.ManyToManyField('self', related_name='categories',symmetrical=False, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Category, self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SpecName(models.Model):
    slug = models.SlugField(primary_key=True)
    name = models.CharField(max_length=127)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='spec_names')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(SpecName, self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Spec(models.Model):
    slug = models.SlugField(primary_key=True)
    value = models.CharField(max_length=80)
    name = models.ForeignKey(SpecName, on_delete=models.CASCADE, related_name='values')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Spec, f'{self.name} {self.value}')
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}: {self.value}'


class Product(CreatedUpdatedModelMixin):
    slug = models.SlugField(primary_key=True, max_length=255)
    name = models.CharField(max_length=247)
    description = models.TextField()
    price = models.PositiveIntegerField()
    available = models.PositiveIntegerField()
    views = models.PositiveIntegerField(default=0)
    cat = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    specs = models.ManyToManyField(Spec, related_name='products', blank=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Product, self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    image = models.ImageField(upload_to='image/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

