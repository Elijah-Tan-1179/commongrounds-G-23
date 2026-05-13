from django.urls import path
from django.shortcuts import redirect
from .views import CommissionListView, CommissionDetailView, CommissionCreateView, CommissionUpdateView, apply_to_job

app_name = 'commissions'

urlpatterns = [
    path('', lambda request: redirect('commission_list')),
    path('requests', CommissionListView.as_view(), name='commission_list'),
    path('request/<int:pk>', CommissionDetailView.as_view(), name='commission_detail'),
    path('request/add', CommissionCreateView.as_view(), name='commission_create'),
    path('request/<int:pk>/edit', CommissionUpdateView.as_view(), name='commission_update'),
    path('job/<int:job_id>/apply', apply_to_job, name='apply_to_job'),
]