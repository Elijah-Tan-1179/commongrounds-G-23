from django.db import models
from django.urls import reverse
from accounts.models import Profile

# Classes and their variables

class CommissionType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Commission(models.Model):
    STATUS_CHOICES = [('Open', 'Open'), ('Full', 'Full')]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.ForeignKey(CommissionType, on_delete=models.SET_NULL, null=True)
    maker = models.ForeignKey(Profile, on_delete=models.CASCADE)
    people_required = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Open')
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('commissions:detail', args=[self.pk])

class Job(models.Model):
    STATUS_CHOICES = [('Open', 'Open'), ('Full', 'Full')]
    
    commission = models.ForeignKey(Commission, on_delete=models.CASCADE, related_name='jobs')
    role = models.CharField(max_length=255)
    manpower_required = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Open')

    class Meta:
        # Sort: Open > Full, then Manpower DESC, then Role ASC
        ordering = ['status', '-manpower_required', 'role']

class JobApplication(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')]
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Sort: Pending > Accepted > Rejected, then date DESC
        ordering = ['status', '-applied_on']