from django.db import models
from guest.models import Employer

class Subscription(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='subscriptions')
    PLAN_CHOICES = [
        ('basic', 'Basic Plan'),
        ('premium', 'Premium Plan'),
        ('enterprise', 'Enterprise Plan'),
    ]
    plan_name = models.CharField(max_length=50, choices=PLAN_CHOICES, default='basic')
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.employer.company_name} - {self.plan_name}"

class Jobposting(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='job_postings')
    job_title = models.CharField(max_length=200)
    job_description = models.TextField()
    location = models.CharField(max_length=100, blank=True, null=True)
    
    # Part-Time Specific Fields
    CATEGORY_CHOICES = [
        ('weekend', 'Weekend Only'),
        ('evening', 'Evening Shift'),
        ('event', 'Event / One-time'),
        ('remote', 'Freelance / Remote'),
        ('flexible', 'Flexible Hours'),
        ('other', 'Other'),
    ]
    part_time_category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='flexible')

    JOB_TYPE_CHOICES = [
        ('online', 'Online / Remote'),
        ('offline', 'Offline / On-site'),
    ]
    job_type = models.CharField(max_length=10, choices=JOB_TYPE_CHOICES, default='offline')
    
    shift_timing = models.CharField(max_length=100, help_text="e.g., 6 PM - 10 PM")
    working_days = models.CharField(max_length=100, help_text="e.g., Saturday & Sunday")
    hourly_pay = models.DecimalField(max_digits=10, decimal_places=2, help_text="Rate per hour", blank=True, null=True)
    
    posted_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()
    salary_range = models.CharField(max_length=100, blank=True, null=True)
    requirements = models.TextField(help_text="Key Responsibilities and Requirements", blank=True, null=True)

    def __str__(self):
        return self.job_title

    class Meta:
        ordering = ['-posted_date']
        verbose_name = 'Job Posting'
        verbose_name_plural = 'Job Postings'
