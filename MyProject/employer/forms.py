from django import forms
from employer.models import Jobposting


class JobPostingForm(forms.ModelForm):
    class Meta:
        model = Jobposting
        fields = ['job_title', 'job_description', 'location', 'work_mode', 'expiry_date', 'salary_range']
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Job Title'}),
            'job_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Job Description', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Location'}),
            'work_mode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Work Mode'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salary_range': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Salary Range'}),
        }
