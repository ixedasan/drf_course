from django.contrib import admin

from recipes.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
