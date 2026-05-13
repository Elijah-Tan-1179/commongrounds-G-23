from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'localevents'

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='localevents:event_list', permanent=False)),
    path('events/', views.EventListView.as_view(), name='event_list'),
    path('event/add/', views.EventCreateView.as_view(), name='event_create'),
    path('event/<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('event/<int:pk>/edit/', views.EventUpdateView.as_view(), name='event_update'),
    path('event/<int:pk>/signup/', views.EventSignupView.as_view(), name='event_signup'),
]
