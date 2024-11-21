from rest_framework import serializers

from recipes.models import Recipe
from recipes.serializers.recipe_ingredient import RecipeIngredientSerializer
from recipes.serializers.recipe_step import RecipeStepSerializer
from recipes.serializers.tag import TagSerializer


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    category_name = serializers.CharField(
        source='category.name',
        read_only=True
    )

    ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    steps = RecipeStepSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'slug', 'category',
            'category_name', 'tags', 'author',
            'description', 'cooking_time',
            'servings', 'difficulty',
            'instructions', 'tips',
            'image', 'video_url',
            'ingredients', 'steps',
            'views_count', 'rating',
            'reviews_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['views_count', 'created_at', 'updated_at']

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / reviews.count()
        return None

    def get_reviews_count(self, obj):
        return obj.reviews.count()