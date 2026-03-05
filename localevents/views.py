from django.shortcuts import render, get_object_or_404
from .models import Event, EventType


def event_list(request):
    """List view for all events."""
    events = Event.objects.all()
    context = {
        'events': events,
    }
    return render(request, 'localevents/event_list.html', context)


def event_detail(request, pk):
    """Detail view for a specific event."""
    event = get_object_or_404(Event, pk=pk)
    context = {
        'event': event,
    }
    return render(request, 'localevents/event_detail.html', context)
