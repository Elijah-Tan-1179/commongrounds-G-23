from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Commission, Job
from .services import CommissionService

class CommissionListView(ListView):
    model = Commission
    template_name = 'commissions/list.html'
    context_object_name = 'commissions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            # froups displayed first 
            context['user_created'] = Commission.objects.filter(maker=profile)
            context['user_applied'] = Commission.objects.filter(jobs__applications__applicant=profile).distinct()
        return context

class CommissionDetailView(DetailView):
    model = Commission
    template_name = 'commissions/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Service used to calc manpower
        context['summary'] = CommissionService.get_commission_summary(self.object)
        return context