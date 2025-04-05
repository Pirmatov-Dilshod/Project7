from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Author, Genre, Book

class BookTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.admin = User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpass')
        
        self.author = Author.objects.create(name='Test Author', bio='Test Bio')
        self.genre = Genre.objects.create(name='Test Genre')
        self.book = Book.objects.create(
            title='Test Book',
            author=self.author,
            published_date='2020-01-01',
            isbn='1234567890123',
            description='Test Description',
            available_copies=5
        )
        self.book.genres.add(self.genre)
    
    def test_get_books(self):
        url = reverse('book-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_book_unauthorized(self):
        url = reverse('book-list')
        data = {
            'title': 'New Book',
            'author': self.author.id,
            'published_date': '2021-01-01',
            'isbn': '9876543210123',
            'description': 'New Description',
            'available_copies': 3,
            'genres': [self.genre.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_book_authorized(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('book-list')
        data = {
            'title': 'New Book',
            'author': self.author.id,
            'published_date': '2021-01-01',
            'isbn': '9876543210123',
            'description': 'New Description',
            'available_copies': 3,
            'genres': [self.genre.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)