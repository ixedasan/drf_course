from rest_framework import serializers

from reviews.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id', 'recipe', 'user', 'username',
            'parent', 'text', 'created_at', 'is_active'
        ]
        read_only_fields = ['created_at']