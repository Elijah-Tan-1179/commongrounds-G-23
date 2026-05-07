from django import forms
from django.forms import inlineformset_factory
from .models import Commission, Job

# Comm Form
class CommissionForm(forms.ModelForm):
    class Meta:
        model = Commission
        exclude = ['maker']
        widgets = {
            'status': forms.Select(),
        }

# Job Form
class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ['commission']
        widgets = {
            'status': forms.Select(),
        }

# FIXED
JobFormSet = inlineformset_factory(
    Commission,
    Job,
    form=JobForm,
    extra=1,
    can_delete=True
)