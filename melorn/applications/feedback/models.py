from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from applications.product.models import Product
from core.models import CreatedUpdatedModelMixin

User = get_user_model()


class Comment(CreatedUpdatedModelMixin):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    body = models.TextField()

    def __str__(self):
        return f"{self.product.name} -> {self.product.price}"


class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="likes")
    is_like = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.owner} liked - {self.product.name}"


class Rating(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="ratings")

    rating = models.SmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ], blank=True, null=True)

    def __str__(self):
        return f"{self.owner} --> {self.product.name}"
