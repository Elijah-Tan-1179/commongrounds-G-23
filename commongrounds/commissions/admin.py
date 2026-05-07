from django.contrib import admin
from .models import CommissionType, Commission, Job, JobApplication


@admin.register(CommissionType)
class CommissionTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


class JobInline(admin.StackedInline):
    model = Job
    extra = 1


class JobApplicationInline(admin.StackedInline):
    model = JobApplication
    extra = 0


@admin.register(Commission)
class CommissionAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'maker', 'people_required', 'status', 'created_on']
    list_filter = ['status', 'type']
    inlines = [JobInline]


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['role', 'commission', 'manpower_required', 'status']
    list_filter = ['status']
    inlines = [JobApplicationInline]


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ['job', 'applicant', 'status', 'applied_on']
    list_filter = ['status']
