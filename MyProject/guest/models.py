from django.db import models
from MyApp.models import District
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
    email = models.EmailField(unique=True, max_length=191)
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
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    area = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Kaloor, Kochi")
    industry = models.CharField(max_length=100, default="General", blank=True, null=True, help_text="e.g., Retail, Education")
    address = models.TextField(blank=True, null=True)
    verification_status = models.BooleanField(default=False)
    
    # New Fields
    profile_picture = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)

    def __str__(self):
        return self.company_name

    def is_profile_complete(self):
        return bool(self.district)

class student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="student_profile",null=True)
    student_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    academic_status = models.CharField(max_length=100, choices=[
        ('diploma', 'Diploma'),
        ('undergraduate', 'Undergraduate'),
        ('postgraduate', 'Postgraduate'),
        ('passout', 'Pass-out'),
    ], default='undergraduate')
    institution_name = models.CharField(max_length=200, blank=True, null=True)
    course_name = models.CharField(max_length=200, blank=True, null=True)
    
    skills = models.TextField(blank=True, null=True)
    
    # New Fields for Part-Time Matching
    AVAILABILITY_CHOICES = [
        ('weekdays_evening', 'Weekdays (Evening)'),
        ('weekends', 'Weekends'),
        ('flexible', 'Flexible'),
        ('10_15_hrs', '10-15 hrs/week'),
    ]
    availability = models.CharField(max_length=50, choices=AVAILABILITY_CHOICES, default="flexible")
    preferred_roles = models.CharField(max_length=500, blank=True, help_text="Multi-select: Web Developer, Tutor, etc.")
    id_card = models.FileField(upload_to='id_cards/', blank=True, null=True)
    
    # Profile Enhancements
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    
    verification_status = models.BooleanField(default=False)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.student_name    

    def is_profile_complete(self):
        return bool(self.district and self.student_name and self.phone_number)

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.email} - {self.message}"

class Feedback(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_feedback')
    recipient = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='received_feedback')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.sender.name}"

class Report(models.Model):
    generated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=100)
    file_path = models.FileField(upload_to='reports/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report_type} - {self.created_at}"
