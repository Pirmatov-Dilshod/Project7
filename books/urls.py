from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView, BookLoanView,
    AuthorListView, AuthorDetailView,
    GenreListView, GenreDetailView
)
from rest_framework.schemas import get_schema_view
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
# Настройки для Swagger
# Настройки для Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="Library API",
      default_version='v1',
      description="API for managing a book library",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@library.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)




router = DefaultRouter()
router.register(r'authors', views.AuthorViewSet, basename='author')
router.register(r'genres', views.GenreViewSet, basename='genre')
router.register(r'books', views.BookViewSet, basename='book')
router.register(r'loans', views.BookLoanViewSet, basename='loan')

urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),
    
    # HTML URLs
    path('', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/add/', BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/edit/', BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
    path('books/<int:pk>/loan/', BookLoanView.as_view(), name='book-loan'),
    
    path('authors/', AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
    
    path('genres/', GenreListView.as_view(), name='genre-list'),
    path('genres/<int:pk>/', GenreDetailView.as_view(), name='genre-detail'),
    
    path('genres/', GenreListView.as_view(), name='genre-list'),
    path('genres/<int:pk>/', GenreDetailView.as_view(), name='genre-detail'),
    
    # Swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]