from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Commission, Job, JobApplication
from .forms import CommissionForm, JobFormSet
from .services import CommissionService

class CommissionListView(ListView):
    model = Commission
    template_name = 'commissions/list.html'
    context_object_name = 'commissions'
    # Sorting prio: Status (Open > Full > Completed > Discontinued), then Created On DESC
    queryset = Commission.objects.order_by('status', '-created_on')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            profile = self.request.user.profile
            # Groups displayed first and removed from the All list
            context['user_created'] = Commission.objects.filter(maker=profile)
            context['user_applied'] = Commission.objects.filter(jobs__applications__applicant=profile).distinct()
        return context

class CommissionDetailView(DetailView):
    model = Commission
    template_name = 'commissions/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Uses service to get manpower summary
        context['summary'] = CommissionService.get_commission_summary(self.object)
        return context

    def post(self, request, *args, **kwargs):
        # Logic for JobApplication form submission
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
        if self.request.POST:
            data['job_formset'] = JobFormSet(self.request.POST)
        else:
            data['job_formset'] = JobFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        job_formset = context['job_formset']
        if job_formset.is_valid():
            # Use Service Layer for atomic creation
            self.object = CommissionService.create_commission(
                author=self.request.user.profile,
                data=form.cleaned_data,
                jobs_data=[f.cleaned_data for f in job_formset if f.cleaned_data]
            )
            return redirect(self.object.get_absolute_url())
        return self.render_to_response(self.get_context_data(form=form))