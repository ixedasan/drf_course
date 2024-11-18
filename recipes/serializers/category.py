from rest_framework import serializers
from recipes.models import Category


class CategorySerializer(serializers.ModelSerializer):
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug',
            'description',
            'recipes_count'
        ]

    def get_recipes_count(self, obj):
        return obj.recipe_set.count()