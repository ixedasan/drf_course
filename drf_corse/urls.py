"""
URL configuration for drf_corse project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from recipes.views import CategoryViewSet, TagViewSet, IngredientViewSet, RecipeViewSet
from reviews.views.comment import CommentViewSet
from reviews.views.review import ReviewViewSet
from users.views import UserViewSet

router = DefaultRouter()

router.register(r'users', UserViewSet)

router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'ingredients', IngredientViewSet)

router.register(r'recipes', RecipeViewSet)

recipes_router = DefaultRouter()
recipes_router.register(r'reviews', ReviewViewSet, basename='recipe-reviews')
recipes_router.register(r'comments', CommentViewSet, basename='recipe-comments')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('recipes/<int:recipe_pk>/', include(recipes_router.urls)),
]

# urlpatterns += router.urls