from rest_framework import serializers

from recipes.models import RecipeIngredient
from recipes.serializers.ingredient import IngredientSerializer


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = RecipeIngredient
        fields = [
            'id', 'ingredient',
            'amount', 'unit', 'notes'
        ]