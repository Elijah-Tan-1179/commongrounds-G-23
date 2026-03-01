from django.contrib import admin
from .models import Genre, Book

"""
This is where the models are registered. This 
is needed so that actual books can be added into the
website.

Admin panel can be accessed with the following details: 
1. username: Zachary
2. email address:  zachary.linus.ong@student.ateneo.edu
3. password: 123456789
"""

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """
    Configuration for the Genre model in the admin
    interface. 
    """
    list_display = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Configuration for the Book model in the admin
    interface. 
    """
    list_display = ('title', 'author', 'publication_year', 'genre')
    list_filter = ('genre','publication_year')
    search_fields = ('title', 'author')

