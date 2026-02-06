from django import forms
from employer.models import Jobposting
from MyApp.models import District, Category


class JobPostingForm(forms.ModelForm):
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Kaloor, Kochi'})
    )

    class Meta:
        model = Jobposting
        fields = ['job_title', 'job_description', 'requirements', 'job_type', 'part_time_category', 'location', 'shift_timing', 'working_days', 'hourly_pay', 'salary_range', 'expiry_date']
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Job Title'}),
            'job_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Job Description', 'rows': 4}),
            'requirements': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Key Responsibilities & Requirements', 'rows': 4}),
            'job_type': forms.Select(attrs={'class': 'form-control w-100'}),
            'part_time_category': forms.Select(attrs={'class': 'form-control w-100'}),
            'shift_timing': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 6 PM - 10 PM'}),
            'working_days': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Weekends Only'}),
            'hourly_pay': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 150', 'step': '0.01'}),
            'salary_range': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 10000-15000'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class EmployerProfileForm(forms.ModelForm):
    industry = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )
    class Meta:
        from guest.models import Employer
        model = Employer
        fields = ['company_name', 'contact_person', 'phone', 'area', 'industry', 'address', 'website', 'profile_picture']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.TextInput(attrs={'class': 'form-control'}),
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
    industry = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )
    website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://company.com'})
    )
    company_logo = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        from guest.models import Employer
        model = Employer
        fields = ['website', 'district', 'area', 'industry', 'description', 'company_logo']
        widgets = {
            'area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Kaloor, Kochi'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your company...'}),
        }
