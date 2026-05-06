from django.db import transaction
from .models import Commission, Job, JobApplication

class CommissionService:
    @staticmethod
    def create_commission(author, data, jobs_data):
        with transaction.atomic():
            commission = Commission.objects.create(maker=author, **data)
            for job_info in jobs_data:
                Job.objects.create(commission=commission, **job_info)
            return commission

    @staticmethod
    def apply_to_job(applicant, job):
        if job.status == 'Full':
            return None
        if JobApplication.objects.filter(job=job, applicant=applicant).exists():
            return None
        return JobApplication.objects.create(job=job, applicant=applicant)

    @staticmethod
    def sync_commission_status(commission):
        all_jobs_full = all(job.status == 'Full' for job in commission.jobs.all())
        if all_jobs_full:
            commission.status = 'Full'
            commission.save()

    @staticmethod
    def get_commission_summary(commission):
        jobs = commission.jobs.all()
        total = sum(j.manpower_required for j in jobs)
        accepted = JobApplication.objects.filter(
            job__commission=commission, 
            status='Accepted'
        ).count()
        return {
            'total_manpower': total,
            'open_manpower': total - accepted
        }