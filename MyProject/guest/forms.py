from django import forms
from django.core.exceptions import ValidationError
import re
from guest.models import Employer, Jobposting, student
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
        fields = ['job_title', 'job_description', 'location', 'work_mode', 'expiry_date', 'salary_range']
        widgets = {
            'job_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Job Title'}),
            'job_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Job Description', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Location'}),
            'work_mode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Work Mode'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'salary_range': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Salary Range'}),
        }



class SignupForm(forms.ModelForm):
    phone_number = forms.CharField(
        label="Phone Number",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone number'
        })
    )
    dob = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        required=False   # optional
    )
    place = forms.CharField(
        label="Place / City",
        required=False,  # optional
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your city'
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        }),
        required=True
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        }),
        required=True
    )
    academic_status = forms.CharField(
        label="Academic Status",
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Final year B.Tech'
        })
    )
    skills = forms.CharField(
        label="Skills",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'List your skills',
            'rows': 4
        })
    )
    id_card = forms.FileField(
        label="Student ID Card",
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control-file'
        })
    )

    class Meta:
        model = student
        fields = ["student_name", "email", "phone_number", "academic_status", "skills", "id_card"]
        widgets = {
            "student_name": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full Name'
            }),
            "email": forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address'
            }),
        }
        labels = {
            "student_name": "Full Name",
            "email": "Email Address",
        }

    def clean_student_name(self):
        name = self.cleaned_data.get("student_name")
        if not name:
            raise ValidationError("Name is required.")
        if not re.match(r'^[A-Za-z\s]+$', name):
            raise ValidationError("Name should only contain letters and spaces.")
        return name

    def clean_phone_number(self):
        phone = self.cleaned_data.get("phone_number")
        if not phone:
            raise ValidationError("Phone number is required.")
        if student.objects.filter(phone_number=phone).exists():
            raise ValidationError("This phone number is already registered.")
        return phone

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if not p1 or not p2:
            raise forms.ValidationError("Both password fields are required.")
        if p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # hashes password

        if commit:
            user.save()

            # Assign default membership card (order=1)

            CustomerProfile.objects.create(
                user=user,
                mobile=self.cleaned_data["mobile"],
                dob=self.cleaned_data.get("dob"),
                place=self.cleaned_data.get("place"),
            )
        return user