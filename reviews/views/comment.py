from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from recipes.models import Recipe
from reviews.models import Comment
from reviews.serializers import CommentSerializer


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        recipe_id = self.kwargs.get('recipe_pk')
        return Comment.objects.filter(recipe_id=recipe_id, is_active=True)

    def perform_create(self, serializer):
        recipe_id = self.kwargs.get('recipe_pk')
        recipe = Recipe.objects.get(id=recipe_id)
        serializer.save(user=self.request.user, recipe=recipe)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)