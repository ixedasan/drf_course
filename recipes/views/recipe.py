from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.viewsets import ModelViewSet

from recipes.filters import RecipeFilter
from recipes.models import Recipe
from recipes.serializers import RecipeCreateUpdateSerializer, RecipeSerializer


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