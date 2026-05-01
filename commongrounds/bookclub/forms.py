from django import forms
from .models import Book, BookReview

class BookContributeForm(forms.ModelForm):
    """
    Form for adding a new book to the library.
    The contributor is pre-set and non-editable.
    """
    class Meta:
        model = Book
        fields = [
            'title', 'author', 'genre', 'synopsis', 
            'publication_year', 'available_to_borrow', 'contributor'
        ]

    def __init__(self, *args, **kwargs):
        # Extracts the user profile passed from the factory
        user_profile = kwargs.pop('user_profile', None)
        super().__init__(*args, **kwargs)
        if user_profile:
            self.fields['contributor'].initial = user_profile
            # Set to disabled to prevent user modification
            self.fields['contributor'].disabled = True


class BookUpdateForm(forms.ModelForm):
    """
    Form for updating existing book details.
    Excludes the contributor field entirely.
    """
    class Meta:
        model = Book
        exclude = ['contributor']


class BookReviewForm(forms.ModelForm):
    """
    Form for submitting book reviews.
    The reviewer is pre-set to the logged-in user and not editable.
    """
    class Meta:
        model = BookReview
        fields = ['title', 'comment', 'user_reviewer']

    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)
        super().__init__(*args, **kwargs)
        if user_profile:
            self.fields['user_reviewer'].initial = user_profile
            self.fields['user_reviewer'].disabled = True


class BookFormFactory:
    """
    Factory class to generate the appropriate form based on context.
    Direct instantiation of form classes in views is restricted.
    """

    @classmethod
    def get_form(cls, context):
        """
        Returns the form class corresponding to the provided context string.
        
        Args:
            context (str): One of 'review', 'contribute', or 'update'.
            
        Returns:
            django.forms.ModelForm: The requested form class.
        """
        forms_map = {
            "review": BookReviewForm,
            "contribute": BookContributeForm,
            "update": BookUpdateForm,
        }
        
        return forms_map.get(context)