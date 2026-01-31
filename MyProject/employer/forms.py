from django import forms
from employer.models import Jobposting
from MyApp.models import District


class JobPostingForm(forms.ModelForm):
    class Meta:
        model = Jobposting
        fields = ['job_title', 'job_description', 'job_type', 'part_time_category', 'location', 'shift_timing', 'working_days', 'hourly_pay', 'salary_range', 'expiry_date']
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Job Title'}),
            'job_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Job Description', 'rows': 4}),
            'job_type': forms.Select(attrs={'class': 'form-control w-100'}),
            'part_time_category': forms.Select(attrs={'class': 'form-control w-100'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Kaloor, Kochi'}),
            'shift_timing': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 6 PM - 10 PM'}),
            'working_days': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Weekends Only'}),
            'hourly_pay': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Rate per hour'}),
            'salary_range': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 10000-15000'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        from guest.models import Employer
        model = Employer
        fields = ['company_name', 'contact_person', 'phone', 'area', 'industry', 'address', 'website', 'profile_picture']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.TextInput(attrs={'class': 'form-control'}),
            'industry': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
        }


class EmployerProfileSetupForm(forms.ModelForm):
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )

    class Meta:
        from guest.models import Employer
        model = Employer
        fields = ['website', 'district', 'area', 'industry', 'address', 'description', 'company_logo', 'profile_picture']
        widgets = {
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://company.com'}),
            'area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Kaloor, Kochi'}),
            'industry': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Retail, IT'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Address', 'rows': 3}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your company...'}),
            'company_logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
