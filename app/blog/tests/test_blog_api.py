"""
Tests for blog APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Blog

from blog.serializers import BlogSerializer


BLOGS_URL = reverse('blog:blog-list')


def create_blog(user, **params):
    """Create and return a sample blog."""
    defaults = {
        'title': 'Sample Blog',
        'description': 'Sample blog description',
    }
    defaults.update(params)

    blog = Blog.objects.create(user=user, **defaults)
    return blog


class PublicBlogAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(BLOGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

