"""
Views for blog APIs.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Blog
from blog import serializers


class BlogViewSet(viewsets.ModelViewSet):
    """View for manage blog APIs."""
    serializer_class = serializers.BlogSerializer
    queryset = Blog.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve the blogs for the authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')
