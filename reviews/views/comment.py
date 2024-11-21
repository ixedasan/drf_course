from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from recipes.models import Recipe
from reviews.models import Comment
from reviews.serializers import CommentSerializer

@extend_schema_view(
    list=extend_schema(
        summary="List Comments",
        description="Retrieve a list of active comments for a specific recipe. Open to authenticated users or read-only access for others.",
        responses={200: CommentSerializer(many=True)},
    ),
    create=extend_schema(
        summary="Create a Comment",
        description="Create a new comment on a recipe. Requires authentication.",
        request=CommentSerializer,
        responses={201: CommentSerializer},
    ),
    update=extend_schema(
        summary="Update a Comment",
        description="Update an existing comment. Requires authentication and that the user is the author of the comment.",
        request=CommentSerializer,
        responses={200: CommentSerializer},
    ),
    partial_update=extend_schema(
        summary="Partially Update a Comment",
        description="Partially update an existing comment. Requires authentication and that the user is the author of the comment.",
        request=CommentSerializer,
        responses={200: CommentSerializer},
    ),
    destroy=extend_schema(
        summary="Delete a Comment",
        description="Delete a comment. Requires authentication and that the user is the author of the comment.",
        responses={204: None},
    ),
)

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