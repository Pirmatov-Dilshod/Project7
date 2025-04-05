from django.contrib import admin
from .models import Author, Genre, Book, BookLoan

class BookInline(admin.TabularInline):
    model = Book
    extra = 1

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date')
    search_fields = ('name',)
    inlines = [BookInline]

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'available_copies')
    list_filter = ('genres', 'author')
    search_fields = ('title', 'author__name', 'isbn')
    filter_horizontal = ('genres',)
    readonly_fields = ('isbn',)

class BookLoanAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'loan_date', 'due_date', 'return_date')
    list_filter = ('loan_date', 'due_date', 'return_date')
    search_fields = ('book__title', 'user__username')
    raw_id_fields = ('book', 'user')

admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookLoan, BookLoanAdmin)