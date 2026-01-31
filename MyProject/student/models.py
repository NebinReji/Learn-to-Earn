from django.db import models


class Application(models.Model):
    student = models.ForeignKey('guest.student', on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey('employer.Jobposting', on_delete=models.CASCADE, related_name='job_applications')
    applied_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
    ], default='pending')
    interview_date = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        # Use related objects instead of the raw id fields to avoid attribute errors
        return f"{self.student.student_name} - {self.job.job_title}"
    

class SkillService(models.Model):
    student = models.ForeignKey('guest.student', on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    CATEGORY_CHOICES = [
        ('tuition', 'Tuition / Teaching'),
        ('technical', 'Technical / Coding'),
        ('creative', 'Creative / Design'),
        ('writing', 'Content / Writing'),
        ('other', 'Other'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Starting Price")
    
    VERIFICATION_CHOICES = [
        ('pending', 'Pending'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]
    verification_status = models.CharField(max_length=20, choices=VERIFICATION_CHOICES, default='pending')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.student.student_name}"

class ServiceBooking(models.Model):
    service = models.ForeignKey(SkillService, on_delete=models.CASCADE, related_name='bookings')
    requester = models.ForeignKey('guest.CustomUser', on_delete=models.CASCADE, related_name='service_requests')
    
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requirements = models.TextField(help_text="Describe your specific needs")
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.service.title} by {self.requester.name}"

class Payment(models.Model):
    booking = models.ForeignKey(ServiceBooking, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default='success')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.transaction_id} for {self.booking}"
    
   
    
class Feedback(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='feedbacks')
    reviewer_role = models.CharField(max_length=10, choices=[('student', 'Student'), ('employer', 'Employer')])
    rating = models.PositiveIntegerField(default=5)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.reviewer_role.capitalize()} Feedback: {self.rating} stars"
