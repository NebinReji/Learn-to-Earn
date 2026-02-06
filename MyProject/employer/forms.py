from django import forms
from django.core.exceptions import ValidationError
from employer.models import Jobposting
from MyApp.models import District, Category
import re


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
            'working_days': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 2-3 days per week'}),
            'hourly_pay': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 150', 'step': '0.01', 'min': '0'}),
            'salary_range': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 10000-15000'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean_job_title(self):
        title = self.cleaned_data.get('job_title', '').strip()
        if len(title) < 3:
            raise ValidationError('Job title must be at least 3 characters long.')
        if len(title) > 200:
            raise ValidationError('Job title must not exceed 200 characters.')
        return title

    def clean_job_description(self):
        desc = self.cleaned_data.get('job_description', '').strip()
        if len(desc) < 10:
            raise ValidationError('Job description must be at least 10 characters long.')
        if len(desc) > 2000:
            raise ValidationError('Job description must not exceed 2000 characters.')
        return desc

    def clean_shift_timing(self):
        timing = self.cleaned_data.get('shift_timing', '').strip()
        if len(timing) < 3:
            raise ValidationError('Shift timing must be specified (e.g., 6 PM - 10 PM).')
        return timing

    def clean_working_days(self):
        days = self.cleaned_data.get('working_days', '').strip()
        if len(days) < 1:
            raise ValidationError('Working days must be specified.')
        return days

    def clean_hourly_pay(self):
        pay = self.cleaned_data.get('hourly_pay')
        if pay is not None:
            if pay < 0:
                raise ValidationError('Hourly pay cannot be negative.')
            if pay > 50000:
                raise ValidationError('Hourly pay cannot exceed ₹50,000.')
        return pay

    def clean_expiry_date(self):
        from django.utils import timezone
        expiry = self.cleaned_data.get('expiry_date')
        if expiry:
            today = timezone.now().date()
            if expiry <= today:
                raise ValidationError('Application deadline must be in the future.')
        return expiry


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

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if phone and not re.match(r'^\d{10}$', phone.replace('-', '').replace(' ', '')):
            raise ValidationError('Phone number must be 10 digits.')
        return phone

    def clean_company_name(self):
        name = self.cleaned_data.get('company_name', '').strip()
        if len(name) < 3:
            raise ValidationError('Company name must be at least 3 characters.')
        return name


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

    def clean_company_logo(self):
        logo = self.cleaned_data.get('company_logo')
        if logo:
            if logo.size > 2 * 1024 * 1024:  # 2MB
                raise ValidationError('Company logo must be less than 2MB.')
            if not logo.name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                raise ValidationError('Logo must be JPG, PNG, or GIF format.')
        return logo

