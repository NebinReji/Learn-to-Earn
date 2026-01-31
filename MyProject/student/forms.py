from django import forms
from guest.models import student
from MyApp.models import District
from .models import Feedback

class StudentProfileForm(forms.ModelForm):
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )

    class Meta:
        model = student
        fields = ['student_name', 'phone_number', 'district', 'academic_status', 'skills', 'availability', 'preferred_roles', 'resume', 'profile_picture', 'bio']
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'district': forms.Select(attrs={'class': 'form-select'}),
            'academic_status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Academic Status'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your skills'}),
            'availability': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Weekends, After 5 PM'}),
            'preferred_roles': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Sales, Data Entry'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell us about yourself'}),
        }


class StudentProfileSetupForm(forms.ModelForm):
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )

    class Meta:
        model = student
        fields = ['district', 'academic_status', 'availability', 'preferred_roles', 'skills', 'bio', 'resume', 'profile_picture']
        widgets = {
            'academic_status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Undergraduate, Final year'}),
            'availability': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Weekends, After 5 PM'}),
            'preferred_roles': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Sales, Data Entry'}),
            'skills': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'List key skills'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short bio...'}),
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }




from .models import SkillService

class SkillServiceForm(forms.ModelForm):
    class Meta:
        model = SkillService
        fields = ['title', 'category', 'description', 'price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Physics Tuition'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your service...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cost per hour/session'}),
        }

from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'review_text']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'review_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your feedback here...'}),
        }
