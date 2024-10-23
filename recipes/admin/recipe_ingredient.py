from django.contrib import admin

from recipes.models import RecipeIngredient


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    pass
