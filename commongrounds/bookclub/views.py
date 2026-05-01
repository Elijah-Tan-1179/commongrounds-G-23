from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from datetime import timedelta

from .models import Book, BookReview, Bookmark, Borrow
from .forms import BookFormFactory

class BookListView(ListView):
    """
    Displays all books, with specialized grouping for authenticated users.
    """
    model = Book
    template_name = 'bookclub/book_list.html'
    context_object_name = 'all_books'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            # Get the user's profile from the accounts app relationship
            profile = user.profile
            
            # Filter books based on user interaction
            context['contributed_books'] = Book.objects.filter(contributor=profile)
            context['bookmarked_books'] = Book.objects.filter(bookmark__profile=profile)
            context['reviewed_books'] = Book.objects.filter(reviews__user_reviewer=profile).distinct()

            # Exclude these from the general list as per specs
            interacted_ids = (
                list(context['contributed_books'].values_list('id', flat=True)) +
                list(context['bookmarked_books'].values_list('id', flat=True)) +
                list(context['reviewed_books'].values_list('id', flat=True))
            )
            context['all_books'] = Book.objects.exclude(id__in=interacted_ids)
        
        return context

class BookDetailView(DetailView):
    """
    Displays book details, reviews, and provides the review form via the factory
    """
    model = Book
    template_name = 'bookclub/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Use Factory to get the review form[cite: 4]
        factory = BookFormFactory()
        form_class = factory.get_form("review")
        
        # Pre-fill profile if logged in[cite: 4]
        if self.request.user.is_authenticated:
            context['review_form'] = form_class(user_profile=self.request.user.profile)
        else:
            context['review_form'] = form_class()
            
        context['bookmarks_count'] = self.object.bookmark_set.count()
        return context

class BookCreateView(LoginRequiredMixin, CreateView):
    """
    Allows 'Book Contributors' to add new books. Uses the Factory Method
    """
    model = Book
    template_name = 'bookclub/book_form.html'

    def get_form_class(self):
        # Obtain form exclusively through the factory
        return BookFormFactory.get_form("contribute")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_profile'] = self.request.user.profile
        return kwargs

    def get_success_url(self):
        # Redirect to the created object's detail view
        return reverse('bookclub:book-detail', kwargs={'pk': self.object.pk})

class BookUpdateView(LoginRequiredMixin, UpdateView):
    """
    Updates book details while excluding the contributor field
    """
    model = Book
    template_name = 'bookclub/book_form.html'

    def get_form_class(self):
        return BookFormFactory.get_form("update")

    def get_success_url(self):
        return reverse('bookclub:book-detail', kwargs={'pk': self.object.pk})

class BookBorrowView(TemplateView):
    """
    Handles book borrowing and calculates return dates
    """
    template_name = 'bookclub/book_borrow.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = get_object_or_404(Book, pk=self.kwargs['pk'])
        return context

    def post(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=self.kwargs['pk'])
        borrow_date = request.POST.get('date_borrowed')
        
        # Return date is always 14 days from borrowing
        return_date = borrow_date + timedelta(days=14)
        
        # Save borrowing record logic goes here
        return redirect('bookclub:book-detail', pk=book.pk)