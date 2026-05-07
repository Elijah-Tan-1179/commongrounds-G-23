from django import forms
from .models import Commission, Job, JobApplication

class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        # Maker is excluded because it is set automatically in the view
        fields = ['title', 'description', 'type', 'people_required', 'status']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['role', 'manpower_required', 'status']

#callows multiple Jobs to be edited on the same page as the Commission
JobFormSet = forms.inlineformset_factory(
    Commission, Job, form=JobForm, extra=1, can_delete=True
)

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [] # applicant is the logged in user