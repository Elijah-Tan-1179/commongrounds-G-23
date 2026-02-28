from django.urls import path
from django.shortcuts import redirect
from .views import ProjectListView, ProjectDetailView

urlpatterns = [
    path('', lambda request: redirect('project_list')),
    path('projects', ProjectListView.as_view(), name = 'project_list'),
    path('project/<int:pk>', ProjectDetailView.as_view(), name='project_detail'),
]