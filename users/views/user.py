from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiExample,
    inline_serializer,
)
from rest_framework import serializers, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer, UserProfileSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List Users",
        description="Retrieve a list of all registered users. Requires authentication.",
        responses={200: UserSerializer(many=True)},
    ),
    retrieve=extend_schema(
        summary="Retrieve User",
        description="Retrieve detailed information about a specific user. Requires authentication.",
        responses={200: UserProfileSerializer},
    ),
    create=extend_schema(
        summary="Create User",
        description="Register a new user. This endpoint is open to all users.",
        request=UserSerializer,
        responses={201: UserSerializer},
    ),
    update=extend_schema(
        summary="Update User",
        description="Update a user's information. Requires authentication.",
        request=UserSerializer,
        responses={200: UserSerializer},
    ),
    partial_update=extend_schema(
        summary="Partially Update User",
        description="Partially update a user's information. Requires authentication.",
        request=UserSerializer,
        responses={200: UserSerializer},
    ),
    destroy=extend_schema(
        summary="Delete User",
        description="Delete a specific user. Requires authentication.",
        responses={204: None},
    ),
)

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'me':
            return UserProfileSerializer
        return UserSerializer

    @extend_schema(
        summary="Retrieve or Update Current User",
        description=(
            "Retrieve details about the currently authenticated user (GET) "
            "or update their profile information (PATCH)."
        ),
        request=UserProfileSerializer,
        responses={
            200: UserProfileSerializer,
            400: inline_serializer(
                name="ErrorResponse",
                fields={"detail": serializers.CharField()},
            ),
        },
    )
    @action(detail=False, methods=['GET', 'PATCH'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        user = request.user

        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        if request.method == 'PATCH':
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @extend_schema(
        summary="Set Password",
        description=(
            "Allows the currently authenticated user to change their password. "
            "Requires the current password (`old_password`) and a new password (`new_password`)."
        ),
        request=inline_serializer(
            name="SetPasswordRequest",
            fields={
                "old_password": serializers.CharField(),
                "new_password": serializers.CharField(),
            },
        ),
        responses={
            204: None,
            400: inline_serializer(
                name="SetPasswordError",
                fields={"old_password": serializers.CharField()},
            ),
        },
    )
    @action(detail=False, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def set_password(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response(
                {"old_password": "Invalid password"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
