from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import EventForm, EventUpdateForm, EventSignupGuestForm
from .models import Event, EventSignup
from accounts.mixins import RoleRequiredMixin  # changed


class EventListView(ListView):
    model = Event
    template_name = 'localevents/event_list.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        created_events = Event.objects.none()
        signed_up_events = Event.objects.none()
        all_events = Event.objects.all()

        if user.is_authenticated:
            profile = user.profile  # changed
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
        })
        return context


class EventDetailView(DetailView):
    model = Event
    template_name = 'localevents/event_detail.html'
    context_object_name = 'event'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        user = self.request.user

        is_owner = False
        if user.is_authenticated:
            is_owner = event.organizer.filter(id=user.profile.id).exists()

        signup_count = event.signups.count()
        is_full = event.event_capacity <= signup_count

        context.update({
            'is_owner': is_owner,
            'signup_count': signup_count,
            'is_full': is_full,
        })
        return context


class EventCreateView(RoleRequiredMixin, LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'localevents/event_form.html'
    required_role = 'Event Organizer'  # added

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Create Event'
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.organizer.add(self.request.user.profile)
        return response

    def get_success_url(self):
        return reverse('localevents:event_detail', args=[self.object.pk])


class EventUpdateView(RoleRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventUpdateForm
    template_name = 'localevents/event_form.html'
    required_role = 'Event Organizer'  # added

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Edit Event'
        return context

    def form_valid(self, form):
        event = form.save(commit=False)
        signup_count = event.signups.count()
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


# ─── Template Method Pattern ─────────────────────────────────────────────────

class BaseSignupView(View):
    def get_event(self):
        return get_object_or_404(Event, pk=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
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

    def check_capacity(self, event):
        return event.signups.count() < event.event_capacity

    def check_ownership(self, event, user):
        if user is None or not user.is_authenticated:
            return True
        return not event.organizer.filter(id=user.profile.id).exists()  # changed

    def create_signup(self, event, user):
        raise NotImplementedError("Subclasses must implement create_signup()")

    def get_redirect_url(self, event):
        return reverse('localevents:event_list')

    def handle_capacity_full(self, event):
        return redirect('localevents:event_detail', pk=event.pk)

    def handle_ownership_denied(self, event):
        return redirect('localevents:event_detail', pk=event.pk)


class EventSignupView(BaseSignupView):
    template_name = 'localevents/event_signup_form.html'

    def get(self, request, *args, **kwargs):
        event = self.get_event()
        if request.user.is_authenticated:
            return redirect('localevents:event_detail', pk=event.pk)
        form = EventSignupGuestForm()
        return render(request, self.template_name, {'event': event, 'form': form})

    def create_signup(self, event, user):
        if user and user.is_authenticated:
            EventSignup.objects.get_or_create(
                event=event,
                user_registrant=user.profile 
            )
            return None

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
        return reverse('localevents:event_detail', args=[event.pk])