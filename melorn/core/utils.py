from typing import Type
from django.db.models import Model
from django.utils.text import slugify
import uuid


def generate_unique_slug(model: Type[Model], to_slug: str) -> str:
    base_slug = slugify(to_slug, allow_unicode=True)
    slug = base_slug
    counter = 0
    while model.objects.filter(slug=slug).exists():
        slug = f'{base_slug}-{uuid.uuid4().hex[:6]}-{counter}'
        counter += 1

    return slug
