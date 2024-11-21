from recipes.models import Recipe, Ingredient, RecipeIngredient, RecipeStep
from recipes.serializers.recipe import RecipeSerializer
from recipes.serializers.recipe_ingredient import RecipeIngredientSerializer
from recipes.serializers.recipe_step import RecipeStepSerializer


class RecipeCreateUpdateSerializer(RecipeSerializer):
    ingredients = RecipeIngredientSerializer(many=True, required=False)
    steps = RecipeStepSerializer(many=True, required=False)

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields

    def create(self, validated_data):
        ingredients_data = self.context.get('ingredients', [])
        steps_data = self.context.get('steps', [])
        tags_data = self.context.get('tags', [])

        recipe = Recipe.objects.create(**validated_data)

        recipe.tags.set(tags_data)

        for ingredient_data in ingredients_data:
            ingredient = Ingredient.objects.get(id=ingredient_data['ingredient'])
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=ingredient_data['amount'],
                unit=ingredient_data['unit']
            )

        for step_data in steps_data:
            RecipeStep.objects.create(recipe=recipe, **step_data)

        return recipe

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        tags_data = self.context.get('tags', [])
        instance.tags.set(tags_data)

        ingredients_data = self.context.get('ingredients', [])
        instance.ingredients.all().delete()
        for ingredient_data in ingredients_data:
            ingredient = Ingredient.objects.get(id=ingredient_data['ingredient'])
            RecipeIngredient.objects.create(
                recipe=instance,
                ingredient=ingredient,
                amount=ingredient_data['amount'],
                unit=ingredient_data['unit']
            )

        steps_data = self.context.get('steps', [])
        instance.steps.all().delete()
        for step_data in steps_data:
            RecipeStep.objects.create(recipe=instance, **step_data)

        return instance