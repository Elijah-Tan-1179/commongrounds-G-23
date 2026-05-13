from django.db import transaction
from .models import Commission, Job, JobApplication


class CommissionService:
    # Comm maker
    @staticmethod
    @transaction.atomic
    def create_commission(author, data, jobs_data):
        commission = Commission.objects.create(
            maker=author,
            **data
        )

        for job_data in jobs_data:
            Job.objects.create(
                commission=commission,
                **job_data
            )

        return commission

    # Job attacher
    @staticmethod
    def apply_to_job(applicant, job):
        existing = JobApplication.objects.filter(
            applicant=applicant,
            job=job
        ).exists()

        if existing:
            raise ValueError(
                'You already applied to this job.'
            )

        accepted_count = JobApplication.objects.filter(
            job=job,
            status=JobApplication.STATUS_ACCEPTED
        ).count()

        if accepted_count >= job.manpower_required:
            raise ValueError(
                'This job is already full.'
            )

        application = JobApplication.objects.create(
            applicant=applicant,
            job=job
        )
        return application

    # sync 
    @staticmethod
    def sync_commission_status(commission):
        jobs = commission.jobs.all()
        if not jobs.exists():
            return

        all_full = all(
            job.status == Job.STATUS_FULL
            for job in jobs
        )

        if all_full:
            commission.status = Commission.STATUS_FULL
        else:
            commission.status = Commission.STATUS_OPEN

        commission.save()

    # Comm data
    @staticmethod
    def get_commission_summary(commission):
        jobs = commission.jobs.all()
        total_manpower = sum(
            job.manpower_required
            for job in jobs
        )

        accepted = JobApplication.objects.filter(
            job__commission=commission,
            status=JobApplication.STATUS_ACCEPTED
        ).count()

        open_manpower = total_manpower - accepted

        return {
            'total_manpower': total_manpower,
            'open_manpower': open_manpower
        }