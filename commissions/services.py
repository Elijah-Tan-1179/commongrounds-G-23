from django.db import transaction
from .models import Commission, Job, JobApplication

# F acilitates logic between

class CommissionService:
    # creates commission entrs
    @staticmethod
    def create_commission(author, data, jobs_data):
        with transaction.atomic():
            commission = Commission.objects.create(maker=author, **data)
            for job_form in jobs_data:
                if job_form.cleaned_data:
                    Job.objects.create(commission=commission, **job_form.cleaned_data)
            return commission

    # attachd to jobs
    @staticmethod
    def apply_to_job(applicant, job):
        if job.status == 'Full':
            return None
        existing = JobApplication.objects.filter(job=job, applicant=applicant).exists()
        if not existing:
            return JobApplication.objects.create(job=job, applicant=applicant)
        return None

    # updateds status
    @staticmethod
    def sync_commission_status(commission):
        all_jobs_full = all(job.status == 'Full' for job in commission.jobs.all())
        if all_jobs_full:
            commission.status = 'Full'
            commission.save()

    # looks at data
    @staticmethod
    def get_commission_summary(commission):
        jobs = commission.jobs.all()
        total = sum(j.manpower_required for j in jobs)
        accepted = JobApplication.objects.filter(job__commission=commission, status='Accepted').count()
        return {
            'total_manpower': total,
            'open_manpower': total - accepted
        }