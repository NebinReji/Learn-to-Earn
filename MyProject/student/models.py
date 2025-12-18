from django.db import models
from guest.models import Jobposting


class Application(models.Model):
    student= models.ForeignKey('guest.student', on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Jobposting, on_delete=models.CASCADE, related_name='job_applications')
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
    
   
