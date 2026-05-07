from django.db import models
from django.urls import reverse
from accounts.models import Profile

# Comm TYPE desc
class CommissionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

# Comm DATA
class Commission(models.Model):
    # Status
    STATUS_OPEN = 'Open'
    STATUS_FULL = 'Full'
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Open'),
        (STATUS_FULL, 'Full'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()

    # FKs
    type = models.ForeignKey(
        CommissionType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    maker = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='commissions_created'
    )

    people_required = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN
    )

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'commissions:commission_detail',
            kwargs={'pk': self.pk}
        )

# Job Data
class Job(models.Model):

    #S tatus
    STATUS_OPEN = 'Open'
    STATUS_FULL = 'Full'
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Open'),
        (STATUS_FULL, 'Full'),
    ]

    # FKs
    commission = models.ForeignKey(
        Commission,
        on_delete=models.CASCADE,
        related_name='jobs'
    )

    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN
    )

    class Meta:
        ordering = ['status', '-manpower_required', 'role']

    def __str__(self):
        return f'{self.role} - {self.commission.title}'

# FK hub
class JobApplication(models.Model):

    # Status
    STATUS_PENDING = 'Pending'
    STATUS_ACCEPTED = 'Accepted'
    STATUS_REJECTED = 'Rejected'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_ACCEPTED, 'Accepted'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    # Fks
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )
    applicant = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name='job_applications'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['status', '-applied_on']

    def __str__(self):
        return f'{self.applicant} -> {self.job}'