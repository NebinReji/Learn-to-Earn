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


class SignupForm(forms.Form):
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

    dob = forms.DateField(
        label="Date of Birth",
        required=True,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )

    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        label="District",
        required=True,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    # ---------------- VALIDATIONS ----------------

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

    # ---------------- SAVE ----------------

    def save(self):
        user = CustomUser.objects.create_user(
            email=self.cleaned_data["email"],
            name=self.cleaned_data["name"],
            password=self.cleaned_data["password1"],
            role='student'
        )
        user.is_active = True  # Step 1 Complete, Login Allowed for Step 2
        user.save()

        student.objects.create(
            user=user,
            student_name=self.cleaned_data["name"],
            email=self.cleaned_data["email"],
            phone_number=self.cleaned_data["phone_number"],
            date_of_birth=self.cleaned_data["dob"],
            district=self.cleaned_data.get("district"),
            # Provide defaults for Step 2 fields to satisfy DB integrity
            bio="",
            skills="",
            preferred_roles="",
            availability="flexible",
            academic_status="undergraduate",
        )

        return user




class EmployerSignupForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm password"})
    )

    terms_agreement = forms.BooleanField(
        label="I agree to the Terms and Conditions",
        required=True,
        error_messages={'required': 'You must agree to the terms to register.'}
    )

    class Meta:
        model = Employer
        fields = [
            "company_name",
            "contact_person",
            "email",
            "phone",
            "website",
            "district",
            "area",
            "industry",
            "address",
            "description",
            "company_logo",
        ]
        widgets = {
            "company_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter company name"}),
            "contact_person": forms.TextInput(attrs={"class": "form-control", "placeholder": "Contact person"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone number"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email address"}),
            "website": forms.URLInput(attrs={"class": "form-control", "placeholder": "https://company.com"}),
            "district": forms.Select(attrs={"class": "form-control"}),
            "area": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Kaloor, Kochi"}),
            "industry": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Retail, IT"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Office address"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Describe your company..."}),
            "company_logo": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(EmployerSignupForm, self).__init__(*args, **kwargs)
        self.fields['website'].required = False
        self.fields['description'].required = False
        self.fields['company_logo'].required = False
        self.fields['district'].required = False

    # ---------- VALIDATION ----------

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

    # ---------- SAVE ----------

    def save(self, commit=True):
        employer = super().save(commit=False)

        user = CustomUser.objects.create_user(
            email=self.cleaned_data["email"],
            name=self.cleaned_data["contact_person"],
            password=self.cleaned_data["password1"],
            role='employer'
        )
        user.is_active = False # Pending Admin Approval
        user.save()

        # Set verification status to False
        employer.verification_status = False

        employer.user = user

        if commit:
            employer.save()

        return employer

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
    