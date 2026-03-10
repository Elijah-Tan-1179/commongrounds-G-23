from django.views.generic import ListView, DetailView

from .models import Book


class BookListView(ListView):
    """
    Renders a list of all books stored in the database.

    Context:
        books: A query of all books, ordered by publication
        year.

    Template:
        bookclub/book_list.html
    """
    model = Book  # used as wrapper for book metadata
    template_name = 'bookclub/book_list.html'
    context_object_name = 'books'


class BookDetailView(DetailView):
    """
    Renders the information for a specific book.

    Context:
        book: The specific book, which is identified by the URL
        primary key

    Template:
        bookclub/book_detail.html
    """
    model = Book
    template_name = 'bookclub/book_detail.html'
    context_object_name = 'book'
