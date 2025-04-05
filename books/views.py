from django.shortcuts import render, redirect
from rest_framework import viewsets, permissions,  filters
from .models import Author, Genre, Book, BookLoan
from .serializers import AuthorSerializer, GenreSerializer, BookSerializer, BookLoanSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('author').prefetch_related('genres')
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    @action(detail=True, methods=['get'])
    def availability(self, request, pk=None):
        book = self.get_object()
        return Response({'available_copies': book.available_copies})

class BookLoanViewSet(viewsets.ModelViewSet):
    queryset = BookLoan.objects.select_related('book', 'user')
    serializer_class = BookLoanSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return BookLoan.objects.all()
        return BookLoan.objects.filter(user=self.request.user)
    
    
class BookViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows books to be viewed or edited.
    
    list:
    Return a list of all books with filtering and search capabilities.
    
    retrieve:
    Return a specific book by ID.
    
    create:
    Create a new book instance (admin only).
    
    update:
    Update an existing book instance (admin only).
    
    partial_update:
    Partially update an existing book instance (admin only).
    
    destroy:
    Delete a book instance (admin only).
    
    availability:
    Check the availability of a specific book.
    """
    ...
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['author', 'genres', 'published_date']
    search_fields = ['title', 'author__name', 'description']
    
class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = super().get_queryset().select_related('author').prefetch_related('genres')
        
        # Фильтрация по автору
        author_id = self.request.GET.get('author')
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        # Фильтрация по жанру
        genre_id = self.request.GET.get('genre')
        if genre_id:
            queryset = queryset.filter(genres__id=genre_id)
        
        # Поиск
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | 
                Q(author__name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['authors'] = Author.objects.all()
        context['genres'] = Genre.objects.all()
        return context

class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'
    
    def get_queryset(self):
        return super().get_queryset().select_related('author').prefetch_related('genres')

class BookCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'genres', 'published_date', 'isbn', 'description', 'cover_image', 'available_copies']
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('book-list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        messages.success(self.request, 'Книга успешно добавлена!')
        return super().form_valid(form)

class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'genres', 'published_date', 'isbn', 'description', 'cover_image', 'available_copies']
    template_name = 'books/book_form.html'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        messages.success(self.request, 'Книга успешно обновлена!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('book-detail', kwargs={'pk': self.object.pk})

class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('book-list')
    
    def test_func(self):
        return self.request.user.is_staff
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Книга успешно удалена!')
        return super().delete(request, *args, **kwargs)

class BookLoanView(LoginRequiredMixin, DetailView):
    model = Book
    template_name = 'books/book_loan.html'
    
    def get(self, request, *args, **kwargs):
        book = self.get_object()
        if book.available_copies > 0:
            BookLoan.objects.create(
                book=book,
                user=request.user,
                due_date=timezone.now() + timezone.timedelta(days=14)
            )
            book.available_copies -= 1
            book.save()
            messages.success(request, f'Вы успешно взяли книгу "{book.title}"!')
        else:
            messages.error(request, 'Извините, эта книга сейчас недоступна.')
        return redirect('book-detail', pk=book.pk)
    
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Регистрация прошла успешно! Теперь вы можете войти.')
        return response
    
class AuthorListView(ListView):
    model = Author
    template_name = 'books/author_list.html'
    context_object_name = 'authors'
    paginate_by = 10

class AuthorDetailView(DetailView):
    model = Author
    template_name = 'books/author_detail.html'
    context_object_name = 'author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(author=self.object)
        return context

class GenreListView(ListView):
    model = Genre
    template_name = 'books/genre_list.html'
    context_object_name = 'genres'
    paginate_by = 20

class GenreDetailView(DetailView):
    model = Genre
    template_name = 'books/genre_detail.html'
    context_object_name = 'genre'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.filter(genres=self.object)
        return context