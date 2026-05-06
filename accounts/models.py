from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # Link to the built-in Django User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Required by specs: Display name (max 63 chars) and Email
    display_name = models.CharField(max_length=63)
    email = models.EmailField()
    
    # Required for Advanced Requirements: Role-based access
    ROLE_CHOICES = [
        ('Market Seller', 'Market Seller'),
        ('Event Organizer', 'Event Organizer'),
        ('Book Contributor', 'Book Contributor'),
        ('Project Creator', 'Project Creator'),
        ('Commission Maker', 'Commission Maker'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    def __str__(self):
        return self.display_name