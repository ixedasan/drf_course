from rest_framework import serializers
from users.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    favorites_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name',
            'last_name', 'avatar', 'bio', 'favorites_count'
        ]

    def get_favorites_count(self, obj):
        return obj.favorites.count()