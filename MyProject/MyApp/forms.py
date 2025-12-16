
from django import forms
from MyApp.models import District,Category, Subcategory

class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = ['district_name']
        widgets = {
            'district_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter District Name'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Category Name'}),
        }

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['subcategory_name', 'category']
        widgets = {
            'subcategory_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Subcategory Name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }