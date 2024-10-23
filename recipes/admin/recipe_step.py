from django.contrib import admin

from recipes.models import RecipeStep


@admin.register(RecipeStep)
class RecipeStepAdmin(admin.ModelAdmin):
    pass
