from django.urls import path
from . import views
from .views import ProfileUpdateView


urlpatterns = [
    path('<str:username>', ProfileUpdateView.as_view(), name='profile_update'),
    path('permission-denied/', views.permission_denied, name='permission_denied'),
]