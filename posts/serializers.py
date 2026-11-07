from rest_framework import serializers

from posts.models import PostModel


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model= PostModel
        fields= ['id', 'title', 'slug', 'content', 'author', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'slug', 'author', 'created_at', 'updated_at']