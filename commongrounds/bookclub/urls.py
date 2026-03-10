from django.urls import path


from .views import BookListView, BookDetailView


# Namespace for the app to allow reverse URL lookups
app_name = 'bookclub'

urlpatterns = [

    # route for the list of all books via (URL: /bookclub/books)
    path('books/', BookListView.as_view(), name='book-list'),

    # route for a specific book's details using its primary key
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),

]

# book list can be accessed via http://127.0.0.1:8000/bookclub/books/