from django import forms
from django.core.exceptions import ValidationError
import re
from guest.models import CustomUser, Employer, student
from MyApp.models import District


class EmployerForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['company_name', 'contact_person', 'phone', 'email', 'area', 'industry', 'address']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Company Name'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Contact Person'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email Address'}),
            'area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Kaloor, Kochi'}),
            'industry': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Retail, IT'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Address', 'rows': 3}),
        }



# -------------------- SIGNUP FORMS (MINIMAL) --------------------

class SignupForm(forms.Form):
    # Minimal Student Signup
    name = forms.CharField(
        label="Full Name",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter full name"})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter email address"})
    )
    phone_number = forms.CharField(
        label="Phone Number",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter phone number"})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm password"})
    )

    def clean_name(self):
        name = self.cleaned_data["name"]
        if not re.match(r"^[A-Za-z\s]+$", name):
            raise ValidationError("Name should contain only letters and spaces.")
        return name

    def clean_email(self):
        email = self.cleaned_data["email"]
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email already registered. Please use a different email.")
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data["phone_number"]
        if student.objects.filter(phone_number=phone).exists():
            raise ValidationError("Phone number already registered.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self):
        # Create minimal user and student profile (mostly empty)
        user = CustomUser.objects.create_user(
            email=self.cleaned_data["email"],
            name=self.cleaned_data["name"],
            password=self.cleaned_data["password1"],
            role='student'
        )
        user.is_active = True
        user.save()

        student.objects.create(
            user=user,
            student_name=self.cleaned_data["name"],
            email=self.cleaned_data["email"],
            phone_number=self.cleaned_data["phone_number"],
            # All other fields are optional and will be filled in profile setup
        )
        return user


class EmployerSignupForm(forms.ModelForm):
    # Minimal Employer Signup
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm password"})
    )

    class Meta:
        model = Employer
        fields = [
            "company_name",
            "contact_person",
            "phone",
            "email",
        ]
        widgets = {
            "company_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter company name"}),
            "contact_person": forms.TextInput(attrs={"class": "form-control", "placeholder": "Contact person"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone number"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email address"}),
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered. Please use a different email.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get("password1") != cleaned_data.get("password2"):
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        employer = super().save(commit=False)
        user = CustomUser.objects.create_user(
            email=self.cleaned_data["email"],
            name=self.cleaned_data["contact_person"],
            password=self.cleaned_data["password1"],
            role='employer'
        )
        user.is_active = True
        user.save()

        employer.user = user
        employer.verification_status = False  # Pending verification
        if commit:
            employer.save()
        return employer


# -------------------- PROFILE SETUP FORMS (DETAILED) --------------------

class StudentProfileForm(forms.ModelForm):
    # Detailed Student Profile Setup
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True
    )
    
    class Meta:
        model = student
        fields = [
             'district', 'academic_status', 'availability', 
            'preferred_roles', 'skills', 'bio', 'resume', 'profile_picture'
        ]
        widgets = {
            "academic_status": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Undergraduate, Final year"}),
            "availability": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Weekends, After 5 PM"}),
            "preferred_roles": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Sales, Data Entry"}),
            "skills": forms.Textarea(attrs={"rows": 3, "class": "form-control", "placeholder": "List key skills"}),
            "bio": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Short bio..."}),
            "resume": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "profile_picture": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

class EmployerProfileForm(forms.ModelForm):
    # This replaces the old generic EmployerForm
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=True
    )

    class Meta:
        model = Employer
        fields = [
            'website', 'district', 'area', 'industry', 'address', 'description', 'company_logo', 'profile_picture'
        ]
        widgets = {
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://company.com'}),
            'area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Kaloor, Kochi'}),
            'industry': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Retail, IT'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Address', 'rows': 3}),
            'description': forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Describe your company..."}),
            'company_logo': forms.ClearableFileInput(attrs={"class": "form-control"}),
            'profile_picture': forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address',
            'required': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'required': True
        })
    )
    