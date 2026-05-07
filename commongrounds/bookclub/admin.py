from django.contrib import admin
from .models import Genre, Book, BookReview, Bookmark, Borrow

"""
This is where the models are registered. This 
is needed so that actual books can be added into the
website.

Admin panel can be accessed with the following details: 
1. username: zachary246208
2. email address:  zachary.linus.ong@student.ateneo.edu
3. password: liklik
"""

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year', 'genre')
    list_filter = ('genre', 'publication_year')
    search_fields = ('title', 'author')

@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    """Allows administrators to manage and moderate book reviews."""
    list_display = ('book', 'user_reviewer', 'title')
    list_filter = ('book',)

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    """Displays which books are saved by specific user profiles."""
    list_display = ('profile', 'book', 'date_bookmarked')

@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    """Tracks active loans and ensures return dates are visible."""
    list_display = ('book', 'borrower', 'date_borrowed', 'date_to_return')
    list_filter = ('date_borrowed', 'date_to_return')
