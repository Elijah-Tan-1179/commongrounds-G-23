from django.db import models # for bundling metadata


class Genre(models.Model):
    """
    Represents a category of books. Has the following
    attributes:

        1. Has a uniqe genre name
        2. Has a description without word limit
    """


    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta: 
        # for sorting genres in alphabetical order (ascending)
        ordering = ['name']

    def __str__(self):
        # return string representation of the genre name
        return self.name
    
class Book(models.Model):
    """Represents an individual book entry within the book club. """


    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    
    """
    Using 'on_delete=models.SET_NULL' as requested to preserve book
    data even if a category is removed. 
    """
    
    # Foreign key to genre; set to null if the genre is deleted
    genre = models.ForeignKey(
        Genre, 
        on_delete=models.SET_NULL,
        null=True,
        related_name='books'
    )

    # Links the book to the user who added it.
    contributor = models.ForeignKey(
        'accounts.Profile',
        on_delete=models.SET_NULL, 
        null=True, 
        related_name = 'contributions'
    )
    synopsis = models.TextField()
    publication_year = models.BooleanField()
    availabe_to_borrow = models.BooleanField(default=True)

    # Timestamps for auditing
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        # Sorts books by publication year, with the most recent being the first
        ordering = ['-publication_year']

    def __str__(self):
        # return string representation of the book title
        return self.title

class BookReview(models.Model):
    """
    Stores reviews. Supports both logged-in and anonymous users.
    """
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )

    # link to a user profile; deleted if the profile is removed
    user_reviewer = models.ForeignKey(
        'accounts.Profile', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    
    # Used when a user is not logged in
    anon_reviewer = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255)
    comment = models.TextField()

    def __str__(self):
        return f"Review for {self.book.title} by {self.user_reviewer or 'Anonymous'}"


class Bookmark(models.Model):
    """
    Allows users to save books to their personal list
    """
    profile = models.ForeignKey(
        'accounts.Profile', 
        on_delete=models.CASCADE, 
        related_name='bookmarks'
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_bookmarked = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile} bookmarked {self.book.title}"


class Borrow(models.Model):
    """
    Manages the lifecycle of a borrowed book
    """
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE, 
        related_name='borrow_records'
    )
    borrower = models.ForeignKey(
        'accounts.Profile', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )
    # Manual name entry for non-logged-in users
    name = models.CharField(max_length=255, null=True, blank=True)
    date_borrowed = models.DateField()
    date_to_return = models.DateField()

    def __str__(self):
        return f"{self.book.title} borrowed by {self.borrower or self.name}"