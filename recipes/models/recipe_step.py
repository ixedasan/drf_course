from django.db import models

from recipes.models import Recipe


class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps')
    order = models.PositiveIntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='recipe_steps/', null=True, blank=True)

