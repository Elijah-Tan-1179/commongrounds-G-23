from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    """Used for Event Create — all fields except organizer (set automatically)."""
    class Meta:
        model = Event
        fields = [
            "title",
            "category",
            "event_image",
            "description",
            "location",
            "start_time",
            "end_time",
            "event_capacity",
            "status",
        ]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class EventUpdateForm(forms.ModelForm):
    """Used for Event Update — excludes organizer; status is auto-managed."""
    class Meta:
        model = Event
        fields = [
            "title",
            "category",
            "event_image",
            "description",
            "location",
            "start_time",
            "end_time",
            "event_capacity",
        ]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class EventSignupGuestForm(forms.Form):
    """Form for unauthenticated users to sign up with their name."""
    new_registrant = forms.CharField(
        max_length=255,
        label="Your Name",
        widget=forms.TextInput(attrs={"placeholder": "Enter your name"}),
    )
