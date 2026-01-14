from django.db import models
from MyApp.models import District

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")
        return self.create_user(email, name, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('employer', 'Employer'),
        ('student', 'Student'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.email








    
class Employer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="employer_profile",null=True)
    company_name = models.CharField(max_length=200)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField(blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='employers')
    address = models.TextField()
    description = models.TextField(blank=True, help_text="About the company")
    verification_status = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name

class student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="student_profile",null=True)
    student_name = models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    academic_status = models.CharField(max_length=100)
    skills = models.TextField()
    bio = models.TextField(blank=True, help_text="Short professional summary")
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    portfolio_link = models.URLField(blank=True, null=True)
    id_card = models.FileField(upload_to='id_cards/')
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')

    def __str__(self):
        return self.student_name    
