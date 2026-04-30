from django.conf import settings
from django.db import models


class Profile(models.Model):
    """User profile for role-based access and event ownership."""
    ROLE_MEMBER = 'Member'
    ROLE_ORGANIZER = 'Event Organizer'
    ROLE_CHOICES = [
        (ROLE_MEMBER, 'Member'),
        (ROLE_ORGANIZER, 'Event Organizer'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default=ROLE_MEMBER)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class EventType(models.Model):
    """Event type/category model."""
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']
        verbose_name = 'Event Type'
        verbose_name_plural = 'Event Types'

    def __str__(self):
        return self.name


class Event(models.Model):
    """Local event model."""
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        EventType,
        on_delete=models.SET_NULL,
        null=True,
        related_name='events'
    )
    organizer = models.ManyToManyField(
        Profile,
        related_name='organized_events',
        blank=True
    )
    event_image = models.ImageField(
        upload_to='localevents/events/',
        null=True,
        blank=True
    )
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    event_capacity = models.PositiveIntegerField(default=1)
    STATUS_AVAILABLE = 'Available'
    STATUS_FULL = 'Full'
    STATUS_DONE = 'Done'
    STATUS_CANCELLED = 'Cancelled'
    STATUS_CHOICES = [
        (STATUS_AVAILABLE, 'Available'),
        (STATUS_FULL, 'Full'),
        (STATUS_DONE, 'Done'),
        (STATUS_CANCELLED, 'Cancelled'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_AVAILABLE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.title


class EventSignup(models.Model):
    """Signup record for an event."""
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='signups'
    )
    user_registrant = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='event_signups'
    )
    new_registrant = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.event.title} signup"
