from django.contrib import admin
from .models import (
    CommissionType,
    Commission,
    Job,
    JobApplication
)


admin.site.register(CommissionType)
admin.site.register(Commission)
admin.site.register(Job)
admin.site.register(JobApplication)