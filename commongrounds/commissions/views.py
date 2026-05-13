from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from accounts.mixins import RoleRequiredMixin
from .models import Commission, Job, JobApplication
from .forms import CommissionForm, JobFormSet
from .services import CommissionService


class CommissionListView(ListView):
    model = Commission
    template_name = 'commissions/list.html'
    context_object_name = 'commissions'

    def get_queryset(self):
        return Commission.objects.all().order_by(
            'status',
            '-created_on'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            profile = user.profile
            created = Commission.objects.filter(
                maker=profile
            )
            applied = Commission.objects.filter(
                jobs__applications__applicant=profile
            ).distinct()

            all_commissions = (
                self.get_queryset()
                .exclude(id__in=created)
                .exclude(id__in=applied)
            )

            context['created_commissions'] = created
            context['applied_commissions'] = applied
            context['all_commissions'] = all_commissions
        return context


class CommissionDetailView(DetailView):
    model = Commission
    template_name = 'commissions/detail.html'
    context_object_name = 'commission'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        summary = CommissionService.get_commission_summary(
            self.object
        )

        context.update(summary)
        jobs_with_status = []

        for job in self.object.jobs.all():

            accepted_count = job.applications.filter(
                status='Accepted'
            ).count()

            is_full = (accepted_count >= job.manpower_required)

            jobs_with_status.append({
                'job': job,
                'accepted_count': accepted_count,
                'is_full': is_full,
            })

        context['jobs_with_status'] = jobs_with_status
        return context


class CommissionCreateView(LoginRequiredMixin, RoleRequiredMixin, CreateView):

    required_role = 'Commission Maker'
    model = Commission
    form_class = CommissionForm
    template_name = 'commissions/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['job_formset'] = JobFormSet(
                self.request.POST
            )
        else:
            context['job_formset'] = JobFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        job_formset = context['job_formset']
        if job_formset.is_valid():
            jobs_data = []

            for job_form in job_formset:

                if job_form.cleaned_data:
                    jobs_data.append({
                        'role': job_form.cleaned_data['role'],
                        'manpower_required': (
                            job_form.cleaned_data[
                                'manpower_required'
                            ]
                        ),
                        'status': (
                            job_form.cleaned_data['status']
                        ),
                    })

            commission = (
                CommissionService.create_commission(
                    author=self.request.user.profile,
                    data=form.cleaned_data,
                    jobs_data=jobs_data
                )
            )
            return redirect(
                commission.get_absolute_url()
            )
        return self.form_invalid(form)


class CommissionUpdateView(LoginRequiredMixin, RoleRequiredMixin, UpdateView):
    required_role = 'Commission Maker'
    model = Commission
    form_class = CommissionForm
    template_name = 'commissions/update.html'
    context_object_name = 'commission'

    def dispatch(self, request, *args, **kwargs):
        commission = self.get_object()
        if commission.maker != request.user.profile:
            return redirect('commissions:commission_detail', pk=commission.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['job_formset'] = JobFormSet(
                self.request.POST,
                instance=self.object
            )

        else:
            context['job_formset'] = JobFormSet(
                instance=self.object
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        job_formset = context['job_formset']

        if job_formset.is_valid():
            self.object = form.save()
            job_formset.instance = self.object
            job_formset.save()

            # Update job statuses
            for job in self.object.jobs.all():
                accepted_count = job.applications.filter(
                    status='Accepted'
                ).count()
                if accepted_count >= job.manpower_required:
                    job.status = 'Full'
                else:
                    job.status = 'Open'

                job.save()
            # Sync commission status
            CommissionService.sync_commission_status(
                self.object
            )
            return redirect(self.object.get_absolute_url())
        return self.form_invalid(form)


@login_required
def apply_to_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    try:
        CommissionService.apply_to_job(
            applicant=request.user.profile,
            job=job
        )

        messages.success(
            request,
            'Successfully applied.'
        )

    except ValueError as error:
        messages.error(request, str(error))
    return redirect(
        'commissions:commission_detail',
        pk=job.commission.pk
    )