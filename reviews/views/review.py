from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from recipes.models import Recipe
from reviews.models import Review
from reviews.serializers import ReviewSerializer

@extend_schema_view(
    list=extend_schema(
        summary="List Reviews",
        description="Retrieve a list of reviews for a specific recipe. Open to authenticated users or read-only access for others.",
        responses={200: ReviewSerializer(many=True)},
    ),
    create=extend_schema(
        summary="Create a Review",
        description="Create a new review for a recipe. Requires authentication.",
        request=ReviewSerializer,
        responses={201: ReviewSerializer},
    ),
    update=extend_schema(
        summary="Update a Review",
        description="Update an existing review. Requires authentication and that the user is the author of the review.",
        request=ReviewSerializer,
        responses={200: ReviewSerializer},
    ),
    partial_update=extend_schema(
        summary="Partially Update a Review",
        description="Partially update an existing review. Requires authentication and that the user is the author of the review.",
        request=ReviewSerializer,
        responses={200: ReviewSerializer},
    ),
    destroy=extend_schema(
        summary="Delete a Review",
        description="Delete a review. Requires authentication and that the user is the author of the review.",
        responses={204: None},
    ),
)

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        recipe_id = self.kwargs.get('recipe_pk')
        return Review.objects.filter(recipe_id=recipe_id)

    def perform_create(self, serializer):
        recipe_id = self.kwargs.get('recipe_pk')
        recipe = Recipe.objects.get(id=recipe_id)
        serializer.save(user=self.request.user, recipe=recipe)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)