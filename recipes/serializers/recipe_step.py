from rest_framework import serializers

from recipes.models import RecipeStep


class RecipeStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeStep
        fields = ['id', 'order', 'description', 'image']