import django_filters
from .models import Recipe


class RecipeFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug')
    tags = django_filters.CharFilter(field_name='tags__slug')
    min_cooking_time = django_filters.NumberFilter(field_name='cooking_time', lookup_expr='gte')
    max_cooking_time = django_filters.NumberFilter(field_name='cooking_time', lookup_expr='lte')

    class Meta:
        model = Recipe
        fields = ['category', 'tags', 'difficulty', 'min_cooking_time', 'max_cooking_time']