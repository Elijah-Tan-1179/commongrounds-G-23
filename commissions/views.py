from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Commission, Job
from .forms import CommissionForm, JobFormSet
from .services import CommissionService

# LIST view
class CommissionListView(ListView):
    model = Commission
    template_name = 'commissions/list.html'
    context_object_name = 'commissions'
    queryset = Commission.objects.order_by('status', '-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            context['user_created'] = Commission.objects.filter(maker=profile)
            context['user_applied'] = Commission.objects.filter(
                jobs__applications__applicant=profile
            ).distinct()
        return context

# DETAILS view
class CommissionDetailView(DetailView):
    model = Commission
    template_name = 'commissions/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['summary'] = CommissionService.get_commission_summary(self.object)
        return context
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        job_id = request.POST.get('job_id')
        job = Job.objects.get(id=job_id)
        CommissionService.apply_to_job(request.user.profile, job)
        return redirect('commissions:detail', pk=self.get_object().pk)

class CommissionCreateView(LoginRequiredMixin, CreateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'commissions/create.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['job_formset'] = JobFormSet(self.request.POST or None)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        job_formset = context['job_formset']
        if job_formset.is_valid():
            self.object = CommissionService.create_commission(
                # reqs for bllal
                author=self.request.user.profile,
                data=form.cleaned_data,
                jobs_data=[f.cleaned_data for f in job_formset if f.cleaned_data]
            )
            return redirect(self.object.get_absolute_url())
        return self.render_to_response(self.get_context_data(form=form))

class CommissionUpdateView(LoginRequiredMixin, UpdateView):
    model = Commission
    form_class = CommissionForm
    template_name = 'commissions/update.html'

# FORM DONT MISPELL
    def form_valid(self, form):
        response = super().form_valid(form)
        CommissionService.sync_commission_status(self.object)
        return response