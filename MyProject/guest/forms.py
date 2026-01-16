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

    dob = forms.DateField(
        label="Date of Birth",
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"})
    )

    place = forms.CharField(
        label="Place",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "City / Town"})
    )

    academic_status = forms.CharField(
        label="Academic Status",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Undergraduate, Final year"})
    )

    availability = forms.CharField(
        label="Availability",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Weekends, After 5 PM"})
    )

    preferred_roles = forms.CharField(
        label="Preferred Roles",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., Sales, Data Entry"})
    )

    skills = forms.CharField(
        label="Skills",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "class": "form-control", "placeholder": "List key skills"})
    )

    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        label="District",
        required=False,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    id_card = forms.FileField(
        label="ID Card (optional)",
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )

    profile_picture = forms.ImageField(
        label="Profile Picture (optional)",
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )

    resume = forms.FileField(
        label="Resume (optional)",
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )

    bio = forms.CharField(
        label="Bio",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Short bio..."})
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Enter password"})
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Confirm password"})
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
        user.is_active = True
        user.save()

        student.objects.create(
            user=user,
            student_name=self.cleaned_data["name"],
            email=self.cleaned_data["email"],
            phone_number=self.cleaned_data["phone_number"],
            district=self.cleaned_data.get("district"),
            academic_status=self.cleaned_data.get("academic_status", ""),
            availability=self.cleaned_data.get("availability", ""),
            preferred_roles=self.cleaned_data.get("preferred_roles", ""),
            skills=self.cleaned_data.get("skills", ""),
            id_card=self.cleaned_data.get("id_card") or "",
            profile_picture=self.cleaned_data.get("profile_picture"),
            resume=self.cleaned_data.get("resume"),
            bio=self.cleaned_data.get("bio", ""),
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

    class Meta:
        model = Employer
        fields = [
            "company_name",
            "contact_person",
            "phone",
            "email",
            "phone",
            "website",
            "district",
            "area",
            "industry",
            "address",
            "description",
            "company_logo",
            "profile_picture",
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
        self.fields['profile_picture'].required = False
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
        user.is_active = True
        user.save()

        # Auto-verify employer for immediate access
        employer.verification_status = True

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
    