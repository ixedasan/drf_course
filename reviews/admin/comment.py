from django.contrib import admin

from reviews.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
