from rest_framework import serializers
from .models import Author, Genre, Book, BookLoan
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name', 'description']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'birth_date']

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    genres = GenreSerializer(many=True)
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genres', 'published_date', 
                  'isbn', 'description', 'cover_image', 'available_copies']

class BookLoanSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    user = UserSerializer()
    
    class Meta:
        model = BookLoan
        fields = ['id', 'book', 'user', 'loan_date', 'due_date', 'return_date']