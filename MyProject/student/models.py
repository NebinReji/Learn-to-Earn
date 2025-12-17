from django.db import models
from guest.models import Jobposting

# Create your models here.
class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    academic_status = models.CharField(max_length=50)
    skills = models.TextField(blank=True, null=True)
    id_card = models.ImageField(upload_to='id_cards/', blank=True, null=True)
    verification_status = models.BooleanField(default=False)

    def __str__(self):
        return self.student_name

# Student applications for jobs
class Application(models.Model):
    application_id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applications')
    job_id = models.ForeignKey(Jobposting, on_delete=models.CASCADE, related_name='applications')
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ], default='pending')
    interview_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.student_id.student_name} - {self.job_id.job_title}"
    
   
