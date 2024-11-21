from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from recipes.models import Tag
from recipes.serializers import TagSerializer

@extend_schema_view(
    list=extend_schema(
        summary="List Tags",
        description="Retrieve a list of all tags. Open to any user.",
        responses={200: TagSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve a Tag",
        description="Retrieve details of a specific tag by its slug. Open to any user.",
        responses={200: TagSerializer},
    ),
    create=extend_schema(
        summary="Create a Tag",
        description="Create a new tag. Requires admin privileges.",
        request=TagSerializer,
        responses={201: TagSerializer},
    ),
    update=extend_schema(
        summary="Update a Tag",
        description="Update an existing tag by its slug. Requires admin privileges.",
        request=TagSerializer,
        responses={200: TagSerializer},
    ),
    partial_update=extend_schema(
        summary="Partially Update a Tag",
        description="Partially update an existing tag by its slug. Requires admin privileges.",
        request=TagSerializer,
        responses={200: TagSerializer},
    ),
    destroy=extend_schema(
        summary="Delete a Tag",
        description="Delete a tag by its slug. Requires admin privileges.",
        responses={204: None},
    ),
)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]