from django.db import models
from MyApp.models import District

# Create your models here.

class Employer(models.Model):
    employer_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='employers')
    address = models.TextField()
    verification_status = models.BooleanField(default=False)

    def __str__(self):
        return self.company_name

class Jobposting(models.Model):
    job_id = models.AutoField(primary_key=True)
    employer_id = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='job_postings')
    job_title = models.CharField(max_length=200)
    job_description = models.TextField()
    location = models.CharField(max_length=100)
    work_mode = models.CharField(max_length=50)
    posted_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()
    salary_range = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return self.job_title    
