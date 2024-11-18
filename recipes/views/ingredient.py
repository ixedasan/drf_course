from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, permissions
from rest_framework.viewsets import ModelViewSet

from recipes.models import Ingredient
from recipes.serializers import IngredientSerializer

@extend_schema_view(
    list=extend_schema(
        summary="List Ingredients",
        description="Retrieve a list of all ingredients. Open to any user.",
        responses={200: IngredientSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve an Ingredient",
        description="Retrieve detailed information about a specific ingredient by its ID. Open to any user.",
        responses={200: IngredientSerializer},
    ),
    create=extend_schema(
        summary="Create an Ingredient",
        description="Create a new ingredient. Requires admin permissions.",
        request=IngredientSerializer,
        responses={201: IngredientSerializer},
    ),
    update=extend_schema(
        summary="Update an Ingredient",
        description="Update an existing ingredient. Requires admin permissions.",
        request=IngredientSerializer,
        responses={200: IngredientSerializer},
    ),
    partial_update=extend_schema(
        summary="Partially Update an Ingredient",
        description="Partially update an existing ingredient. Requires admin permissions.",
        request=IngredientSerializer,
        responses={200: IngredientSerializer},
    ),
    destroy=extend_schema(
        summary="Delete an Ingredient",
        description="Delete an ingredient by its ID. Requires admin permissions.",
        responses={204: None},
    ),
)

class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]