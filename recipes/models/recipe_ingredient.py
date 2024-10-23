from django.db import models

from recipes.models import Recipe, Ingredient


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=50)
    notes = models.CharField(max_length=100, blank=True)


