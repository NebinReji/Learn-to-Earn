from django.db import models
from guest.models import Employer


class Jobposting(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='job_postings')
    job_title = models.CharField(max_length=200)
    job_description = models.TextField()
    location = models.CharField(max_length=100)
    work_mode = models.CharField(max_length=50)
    posted_date = models.DateField(auto_now_add=True)
    expiry_date = models.DateField()
    salary_range = models.CharField(max_length=100)

    def __str__(self):
        return self.job_title

    class Meta:
        ordering = ['-posted_date']
        verbose_name = 'Job Posting'
        verbose_name_plural = 'Job Postings'
