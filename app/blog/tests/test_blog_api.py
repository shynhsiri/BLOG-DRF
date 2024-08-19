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


class PrivateBlogAPITests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrive_blogs(self):
        """Test retrieving a list of blogs."""
        create_blog(user=self.user)
        create_blog(user=self.user)

        res = self.client.get(BLOGS_URL)

        blogs = Blog.objects.all().order_by('-id')
        serializer = BlogSerializer(blogs, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_blog_list_limited_to_user(self):
        """Test blog list is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'testpass123',
        )
        create_blog(user=other_user)
        create_blog(user=self.user)

        res = self.client.get(BLOGS_URL)

        blogs = Blog.objects.filter(user=self.user)
        serializer = BlogSerializer(blogs, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
