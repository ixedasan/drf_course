from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, extend_schema_view
from rest_framework import filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet

from recipes.filters import RecipeFilter
from recipes.models import Recipe
from recipes.serializers import RecipeCreateUpdateSerializer, RecipeSerializer

@extend_schema_view(
    list=extend_schema(
        summary="List Recipes",
        description="Retrieve a list of all recipes with optional filters, search, and ordering. Open to any user.",
        parameters=[
            OpenApiParameter("title", OpenApiTypes.STR, description="Filter by recipe title"),
            OpenApiParameter("description", OpenApiTypes.STR, description="Filter by recipe description"),
            OpenApiParameter("created_at", OpenApiTypes.DATE, description="Order by creation date"),
            OpenApiParameter("cooking_time", OpenApiTypes.INT, description="Order by cooking time"),
            OpenApiParameter("views_count", OpenApiTypes.INT, description="Order by views count"),
        ],
        responses={200: RecipeSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve a Recipe",
        description="Retrieve details of a specific recipe by its ID. Open to any user. Updates the view count.",
        responses={200: RecipeSerializer},
    ),
    create=extend_schema(
        summary="Create a Recipe",
        description="Create a new recipe. Requires authentication.",
        request=RecipeCreateUpdateSerializer,
        responses={201: RecipeSerializer},
    ),
    update=extend_schema(
        summary="Update a Recipe",
        description="Update an existing recipe. Requires authentication.",
        request=RecipeCreateUpdateSerializer,
        responses={200: RecipeSerializer},
    ),
    partial_update=extend_schema(
        summary="Partially Update a Recipe",
        description="Partially update an existing recipe. Requires authentication.",
        request=RecipeCreateUpdateSerializer,
        responses={200: RecipeSerializer},
    ),
    destroy=extend_schema(
        summary="Delete a Recipe",
        description="Delete a recipe by its ID. Requires authentication.",
        responses={204: None},
    ),
    favorite=extend_schema(
        summary="Add or Remove Recipe from Favorites",
        description=(
            "Toggle a recipe as a favorite for the authenticated user. "
            "If the recipe is already in favorites, it will be removed; otherwise, it will be added."
        ),
        responses={200: OpenApiTypes.OBJECT},
    ),
    favorites=extend_schema(
        summary="List Favorite Recipes",
        description="Retrieve a list of all recipes marked as favorites by the authenticated user.",
        responses={200: RecipeSerializer(many=True)},
    ),
)

class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_class = RecipeFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'cooking_time', 'views_count']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return RecipeCreateUpdateSerializer
        return RecipeSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'ingredients': self.request.data.get('ingredients', []),
            'steps': self.request.data.get('steps', []),
            'tags': self.request.data.get('tags', [])
        })
        return context

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        return super().retrieve(request, *args, **kwargs)

    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        recipe = self.get_object()
        user = request.user

        if recipe in user.favorites.all():
            user.favorites.remove(recipe)
            return Response({"detail": "Deleted from favorites"}, status=status.HTTP_200_OK)

        user.favorites.add(recipe)
        return Response({"detail": "Added to favorites"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated])
    def favorites(self, request):
        favorites = request.user.favorites.all()
        serializer = self.get_serializer(favorites, many=True)
        return Response(serializer.data)