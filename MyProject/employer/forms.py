from django import forms
from employer.models import Jobposting
from guest.models import Employer

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = Jobposting
        fields = ['job_title', 'job_description', 'location', 'work_mode', 'working_hours', 'skills_required', 'expiry_date', 'salary_range']
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Job Title'}),
            'job_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Job Description', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Location (Required for Offline)'}),
            'work_mode': forms.Select(attrs={'class': 'form-control'}),
            'working_hours': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 10 hours/week'}),
            'skills_required': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter required skills (comma separated)', 'rows': 3}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salary_range': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Salary Range'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        work_mode = cleaned_data.get('work_mode')
        location = cleaned_data.get('location')

        if work_mode == 'Offline' and not location:
            self.add_error('location', 'Location is required for Offline jobs.')
        
        if work_mode == 'Online' and not location:
             # Auto-fill location for Online jobs if empty
            cleaned_data['location'] = 'Remote / Anywhere'
            
        return cleaned_data

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['company_name', 'company_logo', 'contact_person', 'phone', 'email', 'website', 'district', 'address', 'description']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'company_logo': forms.FileInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Person'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Office Address'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'About the Company'}),
        }
