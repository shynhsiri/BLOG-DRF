"""
Serializers for blog APIs
"""
from rest_framework import serializers

from core.models import Blog


class BlogSerializer(serializers.ModelSerializer):
    """Serializer for blogs."""

    class Meta:
        model = Blog
        fields = ['id', 'title', 'description']
        read_only_fields = ['id']
