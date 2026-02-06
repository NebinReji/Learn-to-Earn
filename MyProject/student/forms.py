from django import forms
from django.core.exceptions import ValidationError
from guest.models import student
from MyApp.models import District
from .models import Feedback
import re

class StudentProfileForm(forms.ModelForm):
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    
    class Meta:
        model = student
        fields = ['student_name', 'phone_number', 'district', 'academic_status', 'skills', 'availability', 'preferred_roles', 'resume', 'profile_picture', 'id_card', 'bio']
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number (10 digits)'}),
            'academic_status': forms.Select(attrs={'class': 'form-select'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter your skills'}),
            'availability': forms.Select(attrs={'class': 'form-select'}),
            'preferred_roles': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Sales, Data Entry'}),
            'resume': forms.FileInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'id_card': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell us about yourself'}),
        }

    def __init__(self, *args, **kwargs):
        super(StudentProfileForm, self).__init__(*args, **kwargs)
        self.fields['bio'].required = False
        self.fields['resume'].required = False
        self.fields['profile_picture'].required = False
        self.fields['id_card'].required = False
        self.fields['district'].required = False

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()
        if phone:
            if not re.match(r'^\d{10}$', phone.replace('-', '').replace(' ', '')):
                raise ValidationError('Phone number must be 10 digits.')
        return phone

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            if resume.size > 5 * 1024 * 1024:  # 5MB
                raise ValidationError('Resume file must be less than 5MB.')
            if not resume.name.endswith(('.pdf', '.doc', '.docx')):
                raise ValidationError('Resume must be PDF, DOC, or DOCX format.')
        return resume

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            if picture.size > 2 * 1024 * 1024:  # 2MB
                raise ValidationError('Profile picture must be less than 2MB.')
            if not picture.name.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                raise ValidationError('Profile picture must be JPG, PNG, or GIF format.')
        return picture

    def clean_id_card(self):
        id_card = self.cleaned_data.get('id_card')
        if id_card:
            if id_card.size > 3 * 1024 * 1024:  # 3MB
                raise ValidationError('ID card file must be less than 3MB.')
            if not id_card.name.endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                raise ValidationError('ID card must be PDF, JPG, or PNG format.')
        return id_card

class StudentProfileSetupForm(forms.ModelForm):
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True
    )
    id_card = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=True,
        label="Upload ID Card (Required for Verification)"
    )
    class Meta:
        model = student
        fields = ['district', 'academic_status', 'availability', 'preferred_roles', 'skills', 'bio', 'resume', 'profile_picture', 'id_card']
        widgets = {
            'academic_status': forms.Select(attrs={'class': 'form-select'}),
            'availability': forms.Select(attrs={'class': 'form-select'}),
            'preferred_roles': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Sales, Data Entry'}),
            'skills': forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'List key skills'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short bio...'}),
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'id_card': forms.ClearableFileInput(attrs={'class': 'form-control'})
        }
    
    def clean_id_card(self):
        id_card = self.cleaned_data.get('id_card')
        if not id_card:
            raise ValidationError('ID card is required for verification.')
        if id_card.size > 3 * 1024 * 1024:  # 3MB
            raise ValidationError('ID card file must be less than 3MB.')
        if not id_card.name.endswith(('.pdf', '.jpg', '.jpeg', '.png')):
            raise ValidationError('ID card must be PDF, JPG, or PNG format.')
        return id_card



from .models import SkillService

class SkillServiceForm(forms.ModelForm):
    class Meta:
        model = SkillService
        fields = ['title', 'category', 'description', 'price']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Physics Tuition'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your service...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cost per hour/session', 'step': '0.01', 'min': '0'}),
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 3:
            raise ValidationError('Service title must be at least 3 characters long.')
        if len(title) > 200:
            raise ValidationError('Service title must not exceed 200 characters.')
        return title
    
    def clean_description(self):
        description = self.cleaned_data.get('description', '').strip()
        if len(description) < 10:
            raise ValidationError('Description must be at least 10 characters long.')
        if len(description) > 2000:
            raise ValidationError('Description must not exceed 2000 characters.')
        return description
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None:
            if price < 0:
                raise ValidationError('Price cannot be negative.')
            if price > 10000:
                raise ValidationError('Price cannot exceed ₹10,000.')
        return price

from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'review_text']
        widgets = {
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'review_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your feedback here...'}),
        }
    
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating is not None:
            if rating < 1 or rating > 5:
                raise ValidationError('Rating must be between 1 and 5.')
        return rating
    
    def clean_review_text(self):
        text = self.cleaned_data.get('review_text', '').strip()
        if len(text) < 5:
            raise ValidationError('Review must be at least 5 characters long.')
        if len(text) > 1000:
            raise ValidationError('Review must not exceed 1000 characters.')
        return text
