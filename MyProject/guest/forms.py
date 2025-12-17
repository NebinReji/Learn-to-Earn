from django import forms
from guest.models import Employer, Jobposting
from MyApp.models import District

class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['company_name', 'contact_person', 'phone', 'email', 'district', 'address']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Company Name'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Contact Person'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email Address'}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Address', 'rows': 3}),
        }

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = Jobposting
        fields = ['employer_id', 'job_title', 'job_description', 'location', 'work_mode', 'expiry_date', 'salary_range']
        widgets = {
            'employer_id': forms.Select(attrs={'class': 'form-control'}),
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Job Title'}),
            'job_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Job Description', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Location'}),
            'work_mode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Work Mode'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salary_range': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Salary Range'}),
        }
