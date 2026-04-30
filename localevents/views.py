from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import EventForm, EventUpdateForm, EventSignupGuestForm
from .models import Event, EventSignup, Profile


def get_or_create_profile(user):
    if not user or not user.is_authenticated:
        return None
    profile, _ = Profile.objects.get_or_create(
        user=user,
        defaults={"role": Profile.ROLE_MEMBER}
    )
    return profile


class OrganizerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        profile = get_or_create_profile(self.request.user)
        return profile is not None and profile.role == Profile.ROLE_ORGANIZER

    def handle_no_permission(self):
        return redirect('localevents:event_list')


class EventListView(ListView):
    model = Event
    template_name = 'localevents/event_list.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_or_create_profile(self.request.user)

        created_events = Event.objects.none()
        signed_up_events = Event.objects.none()
        all_events = Event.objects.all()

        if profile:
            created_events = all_events.filter(organizer=profile)
            signed_up_events = all_events.filter(
                signups__user_registrant=profile
            ).exclude(organizer=profile)
            excluded_ids = set(created_events.values_list('id', flat=True))
            excluded_ids |= set(signed_up_events.values_list('id', flat=True))
            all_events = all_events.exclude(id__in=excluded_ids)

        context.update({
            'created_events': created_events.distinct(),
            'signed_up_events': signed_up_events.distinct(),
            'events': all_events.distinct(),
            'can_create': profile is not None and profile.role == Profile.ROLE_ORGANIZER,
        })
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'localevents/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        profile = get_or_create_profile(self.request.user)

        is_owner = profile is not None and event.organizer.filter(id=profile.id).exists()
        signup_count = event.signups.count()
        is_full = event.event_capacity <= signup_count

        context.update({
            'is_owner': is_owner,
            'signup_count': signup_count,
            'is_full': is_full,
        })
        return context


class EventCreateView(LoginRequiredMixin, OrganizerRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'localevents/event_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Create Event'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        profile = get_or_create_profile(self.request.user)
        if profile:
            self.object.organizer.add(profile)
        return response

    def get_success_url(self):
        return reverse('localevents:event_detail', args=[self.object.pk])


class EventUpdateView(LoginRequiredMixin, OrganizerRequiredMixin, UpdateView):
    model = Event
    form_class = EventUpdateForm
    template_name = 'localevents/event_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Event'
        return context

    def form_valid(self, form):
        event = form.save(commit=False)
        signup_count = event.signups.count()
        # Auto-manage status based on capacity
        if signup_count >= event.event_capacity:
            event.status = Event.STATUS_FULL
        else:
            event.status = Event.STATUS_AVAILABLE
        event.save()
        form.save_m2m()
        self.object = event
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('localevents:event_detail', args=[self.object.pk])


# ─── Template Method Pattern ────────────────────────────────────────────────

class BaseSignupView(View):
    """
    Abstract base CBV implementing the Template Method pattern for event signup.

    Subclasses must implement create_signup(). Other steps can be overridden
    to customise behaviour.
    """

    def get_event(self):
        return get_object_or_404(Event, pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        """Template method — defines the skeleton of the signup algorithm."""
        event = self.get_event()
        user = request.user if request.user.is_authenticated else None

        if not self.check_capacity(event):
            return self.handle_capacity_full(event)

        if not self.check_ownership(event, user):
            return self.handle_ownership_denied(event)

        response = self.create_signup(event, user)
        if isinstance(response, HttpResponse):
            return response

        return redirect(self.get_redirect_url(event))

    # ── Steps (each overridable) ──────────────────────────────────────────

    def check_capacity(self, event):
        """Returns True if signup is still allowed (not at capacity)."""
        return event.signups.count() < event.event_capacity

    def check_ownership(self, event, user):
        """Returns True if the user is NOT the organizer of the event."""
        profile = get_or_create_profile(user)
        if profile is None:
            return True
        return not event.organizer.filter(id=profile.id).exists()

    def create_signup(self, event, user):
        """Creates the signup record. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement create_signup()")

    def get_redirect_url(self, event):
        """Returns the URL to redirect to after a successful signup."""
        return reverse('localevents:event_list')

    def handle_capacity_full(self, event):
        return redirect('localevents:event_detail', pk=event.pk)

    def handle_ownership_denied(self, event):
        return redirect('localevents:event_detail', pk=event.pk)


class EventSignupView(BaseSignupView):
    """
    Concrete signup view for Local Events.

    - Logged-in users: POST directly signs them up.
    - Anonymous users: GET shows a name form; POST processes it.

    Demonstrates the Template Method pattern by overriding get_redirect_url()
    to redirect to the event detail page instead of the list.
    """
    template_name = 'localevents/event_signup_form.html'

    def get(self, request, *args, **kwargs):
        """Show the name form for unauthenticated users only."""
        event = self.get_event()
        if request.user.is_authenticated:
            # Logged-in users sign up via POST from the detail page
            return redirect('localevents:event_detail', pk=event.pk)
        form = EventSignupGuestForm()
        return render(request, self.template_name, {'event': event, 'form': form})

    def create_signup(self, event, user):
        """Create signup for logged-in user or guest by name."""
        if user and user.is_authenticated:
            profile = get_or_create_profile(user)
            if profile:
                EventSignup.objects.get_or_create(
                    event=event,
                    user_registrant=profile
                )
            return None

        # Guest signup — validate the name form
        form = EventSignupGuestForm(self.request.POST)
        if not form.is_valid():
            return render(
                self.request,
                self.template_name,
                {'event': event, 'form': form},
            )
        EventSignup.objects.create(
            event=event,
            new_registrant=form.cleaned_data['new_registrant'],
        )
        return None

    def get_redirect_url(self, event):
        """Override: redirect to event detail instead of the list."""
        return reverse('localevents:event_detail', args=[event.pk])
