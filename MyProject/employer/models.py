from django.db import models
from guest.models import Employer


class Jobposting(models.Model):
    JOB_TYPE_CHOICES = [
        ('Online', 'Online'),
        ('Offline', 'Offline'),
    ]

    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='job_postings')
    job_title = models.CharField(max_length=200)
    job_description = models.TextField()
    location = models.CharField(max_length=100, blank=True, null=True, help_text="Required for Offline jobs")
    work_mode = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)
    working_hours = models.CharField(max_length=100, default='Part Time', help_text='e.g., 10 hours/week')
    skills_required = models.TextField(default='', help_text='List required skills separated by commas')
    posted_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()
    salary_range = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.job_title

    class Meta:
        ordering = ['-posted_date']
        verbose_name = 'Job Posting'
        verbose_name_plural = 'Job Postings'


class SubscriptionPlan(models.Model):
    emp = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='subscription_plans')
    plan_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    features = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['price']
        verbose_name = 'Subscription Plan'
        verbose_name_plural = 'Subscription Plans'
