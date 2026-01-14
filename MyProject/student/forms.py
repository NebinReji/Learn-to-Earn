from django import forms
from guest.models import student

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = student
        fields = ['student_name', 'phone_number', 'profile_picture', 'academic_status', 'skills', 'bio', 'resume', 'portfolio_link', 'district', 'id_card']
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'academic_status': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Undergraduate'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List your skills'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short professional summary'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'portfolio_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'district': forms.Select(attrs={'class': 'form-control'}),
            'id_card': forms.FileInput(attrs={'class': 'form-control'}),
        }
