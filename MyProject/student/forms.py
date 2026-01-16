from django import forms
from guest.models import student

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = student
        fields = ['student_name', 'phone_number', 'academic_status', 'skills', 'availability', 'preferred_roles', 'resume', 'profile_picture', 'bio']
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'academic_status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Academic Status'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your skills'}),
            'availability': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Weekends, After 5 PM'}),
            'preferred_roles': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Sales, Data Entry'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell us about yourself'}),
        }



