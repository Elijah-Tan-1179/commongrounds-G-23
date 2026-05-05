from django.urls import path
from .views import ProfileUpdateView


urlpatterns = [
    path('accounts/<str:display_name>', ProfileUpdateView.as_view(), name='profile_update')
]