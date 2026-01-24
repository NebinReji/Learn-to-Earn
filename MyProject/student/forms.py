from django import forms
from guest.models import student
from .models import Feedback

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = student
        fields = [
            'institution_name', 'course_name', 'academic_status', 
            'availability', 'preferred_roles', 'skills', 
            'bio', 'resume', 'profile_picture', 'id_card'
        ]
        widgets = {
            'institution_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your institution name'}),
            'course_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your course/major'}),
            'academic_status': forms.Select(attrs={'class': 'form-select'}),
            'availability': forms.Select(attrs={'class': 'form-select'}),
            'preferred_roles': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Web Developer, Tutor (comma separated)'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'List your key skills'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell us about yourself'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'id_card': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(StudentProfileForm, self).__init__(*args, **kwargs)
        self.fields['bio'].required = False
        self.fields['resume'].required = False
        self.fields['profile_picture'].required = False





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
