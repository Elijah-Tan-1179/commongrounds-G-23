from django.urls import path
from .views import CommissionListView, CommissionDetailView, CommissionCreateView, CommissionUpdateView

app_name = 'commissions'

urlpatterns = [
    path('requests', CommissionListView.as_view(), name='list'),
    path('request/<int:pk>', CommissionDetailView.as_view(), name='detail'),
    path('request/add', CommissionCreateView.as_view(), name='create'),
    path('request/<int:pk>/edit', CommissionUpdateView.as_view(), name='update'),
]