from rest_framework import serializers

from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'recipe', 'user', 'username',
            'rating', 'text', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']