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

    def __string__(self):
        # return string representation of the genre name
        return self.name
    
class Book(models.Model):
    """
    Represents an individual book entry within the book club.
    Has the following attributes:

        1. Book title
        2. Book genre (Based on the Genre Model; If the genre is 
        deleted, this field is NULL)
        3. Book author
        4. Timestamp of when the book entry was first created.
        5. Timestamp of the last time the book entry was modified.
    """
    title = models.CharField(max_length=255)
    """
    Using 'on_delete=models.SET_NULL' as requested to preserve book
    data even if a category is removed. 
    """
    
    genre = models.ForeignKey(
        Genre, 
        on_name='books', 
        on_delete=models.SET_NULL,
        null=True
    )
    author = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publication year']

    def __string__(self):
        # return string representation of the book title
        return self.title
