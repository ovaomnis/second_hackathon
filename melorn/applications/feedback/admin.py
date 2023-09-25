from django.contrib import admin

from applications.feedback.models import Rating, Comment

admin.site.register(Comment)
admin.site.register(Rating)
