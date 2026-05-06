from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Commission, Job
from .services import CommissionService

# for the list
class CommissionListView(ListView):
    model = Commission
    template_name = 'commissions/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            context['user_commissions'] = Commission.objects.filter(maker=profile)
            context['applied_commissions'] = Commission.objects.filter(jobs__applications__applicant=profile).distinct()
        return context

# for the variables
class CommissionDetailView(DetailView):
    model = Commission
    template_name = 'commissions/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = CommissionService()
        context['summary'] = service.get_commission_summary(self.object)
        return context

    def post(self, request, *args, **kwargs):
        # handles job logic
        pass