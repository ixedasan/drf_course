from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, permissions
from rest_framework.viewsets import ModelViewSet

from recipes.models import Category
from recipes.serializers import CategorySerializer


@extend_schema_view(
    list=extend_schema(
        summary="List Categories",
        description="Retrieve a list of all categories. Open to any user.",
        responses={200: CategorySerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve a Category",
        description="Retrieve detailed information about a specific category by its slug. Open to any user.",
        responses={200: CategorySerializer},
    ),
    create=extend_schema(
        summary="Create a Category",
        description="Create a new category. Requires admin permissions.",
        request=CategorySerializer,
        responses={201: CategorySerializer},
    ),
    update=extend_schema(
        summary="Update a Category",
        description="Update an existing category. Requires admin permissions.",
        request=CategorySerializer,
        responses={200: CategorySerializer},
    ),
    partial_update=extend_schema(
        summary="Partially Update a Category",
        description="Partially update an existing category. Requires admin permissions.",
        request=CategorySerializer,
        responses={200: CategorySerializer},
    ),
    destroy=extend_schema(
        summary="Delete a Category",
        description="Delete a category by its slug. Requires admin permissions.",
        responses={204: None},
    ),
)
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]
