from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from employer.models import Jobposting
from guest.models import student, Notification
from student.models import Application, SkillService
from student.forms import StudentProfileForm, StudentProfileSetupForm


# Helper function to get notification data for context
def get_notification_context(user):
    """Returns notification data for navbar"""
    return {
        'recent_notifications': Notification.objects.filter(user=user).order_by('-timestamp')[:5],
        'unread_notifications_count': Notification.objects.filter(user=user, is_read=False).count()
    }



def index(request):
    try:
        stud = student.objects.get(user_id=request.user.id)
        
        if not stud.is_profile_complete():
             return redirect('student_profile_setup')
             
        if not stud.verification_status:
             return redirect('student_verification_pending')
             
        applications_count = Application.objects.filter(student=stud).count()
        my_skills_count = SkillService.objects.filter(student=stud).count()
        
        # Profile Completion Logic
        completion = 20 # Base for account
        if stud.district: completion += 20
        if stud.skills: completion += 20
        if stud.bio: completion += 20
        if stud.resume: completion += 20
        
        recent_jobs = Jobposting.objects.select_related('employer').all().order_by('-id')[:6]
        available_skills = SkillService.objects.exclude(student=stud).select_related('student').order_by('-id')[:4]
        recent_applications = Application.objects.filter(student=stud).select_related('job', 'job__employer').order_by('-applied_date')[:5]
        
        # Get list of applied job IDs
        applied_job_ids = Application.objects.filter(student=stud).values_list('job_id', flat=True)

        # Dashboard Widgets
        notification_context = get_notification_context(request.user)

        context = {
            'applications_count': applications_count,
            'my_skills_count': my_skills_count,
            'profile_completion': completion,
            'recent_jobs': recent_jobs,
            'available_skills': available_skills,
            'recent_applications': recent_applications,
            'applied_job_ids': applied_job_ids,
            **notification_context,  # Add notification data
        }
        return render(request, 'student/index.html', context)
    except student.DoesNotExist:
        return redirect('student_profile_setup')


def complete_profile(request):
    try:
        stud = student.objects.get(user_id=request.user.id)
    except student.DoesNotExist:
        return redirect('student_index')

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=stud)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile completed successfully! Welcome to your dashboard.")
            return redirect('student_index')
    else:
        form = StudentProfileForm(instance=stud)
    
    return render(request, 'student/complete_profile.html', {'form': form})


def view_jobs(request):
    # Restrict access if not verified
    if request.user.is_authenticated:
        try:
            stud = student.objects.get(user_id=request.user.id)
            if stud.is_profile_complete() and not stud.verification_status:
                messages.warning(request, "Please wait for account verification.")
                return redirect('student_verification_pending')
        except student.DoesNotExist:
            pass

    jobs = Jobposting.objects.select_related('employer').all()
    
    # Get applied jobs if user is a student
    applied_job_ids = []
    if request.user.is_authenticated:
        try:
            stud = student.objects.get(user_id=request.user.id)
            applied_job_ids = Application.objects.filter(student=stud).values_list('job_id', flat=True)
        except student.DoesNotExist:
            pass
    
    context = {
        'jobs': jobs,
        'applied_job_ids': applied_job_ids,
    }
    if request.user.is_authenticated:
        context.update(get_notification_context(request.user))
    return render(request, 'student/viewjobs.html', context)


def job_detail(request, job_id):
    job = get_object_or_404(Jobposting.objects.select_related('employer'), id=job_id)

    has_applied = False
    if request.user.is_authenticated:
        try:
            stud = student.objects.get(user_id=request.user.id)
            has_applied = Application.objects.filter(student=stud, job=job).exists()
        except student.DoesNotExist:
            pass
            
    return render(request, 'student/job_detail.html', {'job': job, 'has_applied': has_applied})


def apply_job(request, job_id):
    user_id = request.user.id
    try:
        stud = student.objects.get(user_id=user_id)
    except student.DoesNotExist:
        messages.error(request, "User profile not found. Please complete setup.")
        return redirect('student_profile_setup')
    
    # 1. Check if profile is complete (District is a mandatory field for "completion")
    if not stud.is_profile_complete():
        messages.error(request, "Please complete your profile details first.")
        return redirect('student_profile_setup')

    # 2. Check Verification Status
    if not stud.verification_status:
        # If profile is complete but not verified
        messages.warning(request, "Your profile is under verification. You can apply for jobs once verified.")
        return redirect('student_verification_pending')

    # Check if already applied
    if Application.objects.filter(student=stud, job_id=job_id).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('student_job_detail', job_id=job_id)
    
    # Create application
    job = get_object_or_404(Jobposting, id=job_id)
    Application.objects.create(student=stud, job=job)
    messages.success(request, "Successfully applied for the job!")

    # Notifications
    from guest.models import Notification
    Notification.objects.create(
        user=job.employer.user,
        message=f"New application from {stud.student_name} for {job.job_title}.",
        link='/employer/applications/'
    )
    Notification.objects.create(
        user=request.user,
        message=f"You applied for {job.job_title} at {job.employer.company_name}.",
        link='/student/my-applications/'
    )
    
    return redirect('student_job_detail', job_id=job_id)


def profile(request):
    user_id = request.user.id
    # Auto-create if missing to prevent 404
    stud, created = student.objects.get_or_create(
        user_id=user_id,
        defaults={
            'student_name': request.user.name,
            'email': request.user.email,
            'phone_number': '',
        }
    )
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=stud)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('student_profile')
    else:
        form = StudentProfileForm(instance=stud)
    
    context = {
        'form': form,
        'student': stud,
        **get_notification_context(request.user)
    }
    return render(request, 'student/profile.html', context)

def profile_setup(request):
    user_id = request.user.id
    # Auto-create if missing to prevent 404
    stud, created = student.objects.get_or_create(
        user_id=user_id,
        defaults={
            'student_name': request.user.name,
            'email': request.user.email,
            'phone_number': '',
        }
    )
    
    if request.method == 'POST':
        form = StudentProfileSetupForm(request.POST, request.FILES, instance=stud)
        if form.is_valid():
            stud = form.save(commit=False)
            stud.verification_status = False # Ensure it remains False until Admin approves
            # ID Card is handled by form.save() due to request.FILES
            stud.save()
            
            messages.info(request, "Profile setup complete. Your account is pending Admin verification.")
            return redirect('student_verification_pending')
    else:
        form = StudentProfileSetupForm(instance=stud)
    
    return render(request, 'student/profile_setup.html', {'form': form})


def verification_pending(request):
    return render(request, 'student/verification_pending.html')

def notifications(request):
    from guest.models import Notification
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')[:50]
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()

    # Mark as read after capturing unread count
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)

    return render(request, 'student/notifications.html', {
        'notifications': notifications,
        'unread_count': unread_count,
    })


def my_applications(request):
    user_id = request.user.id
    # Auto-create/Get
    stud, created = student.objects.get_or_create(
        user_id=user_id,
        defaults={
            'student_name': request.user.name or "Student",
            'email': request.user.email,
            'phone_number': '',
        }
    )
    
    if not stud.verification_status:
        messages.warning(request, "Your profile is under verification.")
        return redirect('student_verification_pending')

    applications = Application.objects.filter(student=stud).select_related('job', 'job__employer').order_by('-applied_date')
    context = {
        'applications': applications,
        **get_notification_context(request.user)
    }
    return render(request, 'student/my_applications.html', context)

from student.forms import FeedbackForm
from student.models import Feedback

def review_employer(request, application_id):
    """Student provides feedback about the employer"""
    application = get_object_or_404(Application, id=application_id)
    
    # Verify student owns the application
    if application.student.user != request.user:
        messages.error(request, "Unauthorized")
        return redirect('student_my_applications')
    
    # Check if feedback already exists from student
    existing_feedback = Feedback.objects.filter(
        application=application,
        reviewer_role='student'
    ).first()
        
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=existing_feedback)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.application = application
            feedback.reviewer_role = 'student'
            feedback.save()
            messages.success(request, "Feedback submitted successfully!")
            
            # Send notification to employer
            from guest.models import Notification
            if existing_feedback:
                # Updated feedback
                notification_message = f"{application.student.student_name} has updated their feedback for the '{application.job.job_title}' job."
            else:
                # New feedback
                notification_message = f"{application.student.student_name} has shared feedback about your job '{application.job.job_title}' (Rating: {feedback.rating}⭐)."
            
            Notification.objects.create(
                user=application.job.employer.user,
                message=notification_message,
                link=f'/employer/application/{application.id}/view/'
            )
            
            return redirect('student_my_applications')
    else:
        form = FeedbackForm(instance=existing_feedback)
    
    context = {
        'form': form,
        'application': application,
        'existing_feedback': existing_feedback
    }
    return render(request, 'student/review_employer.html', context)


def view_application_feedback(request, application_id):
    """View all feedback for an application (student view)"""
    application = get_object_or_404(Application, id=application_id)
    
    # Verify student owns the application
    if application.student.user != request.user:
        messages.error(request, "Unauthorized")
        return redirect('student_my_applications')
    
    # Get all feedback for this application
    employer_feedbacks = Feedback.objects.filter(
        application=application,
        reviewer_role='employer'
    )
    student_feedbacks = Feedback.objects.filter(
        application=application,
        reviewer_role='student'
    )
    
    context = {
        'application': application,
        'employer_feedbacks': employer_feedbacks,
        'student_feedbacks': student_feedbacks,
    }
    return render(request, 'student/application_feedback.html', context)


# -------------------- Skills & Services Views --------------------

from .models import SkillService, ServiceBooking
from .forms import SkillServiceForm

def add_skill(request):
    user_id = request.user.id
    # Auto-create/Get
    stud, created = student.objects.get_or_create(
        user_id=user_id,
        defaults={
            'student_name': request.user.name or "Student",
            'email': request.user.email,
            'phone_number': '',
        }
    )
    
    if not stud.is_profile_complete():
        messages.error(request, "Please complete your profile details first.")
        return redirect('student_profile_setup')

    if not stud.verification_status:
        messages.warning(request, "Your profile is under verification. You can add skills once verified.")
        return redirect('student_verification_pending')
    if request.method == 'POST':
        form = SkillServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.student = stud
            service.save()
            messages.success(request, "Skill Service added successfully!")
            
            # Send notification
            from guest.models import Notification
            Notification.objects.create(
                user=request.user,
                message=f"Your skill service '{service.title}' has been created and is pending verification.",
                link='/student/my-skills/'
            )
            
            return redirect('my_skills')
    else:
        form = SkillServiceForm()
        
    return render(request, 'student/add_skill.html', {'form': form})

def my_skills(request):
    user_id = request.user.id
    # Auto-create/Get
    stud, created = student.objects.get_or_create(
        user_id=user_id,
        defaults={
            'student_name': request.user.name or "Student",
            'email': request.user.email,
            'phone_number': '',
        }
    )
    
    if not stud.verification_status:
        messages.warning(request, "Your profile is under verification.")
        return redirect('student_verification_pending')

    services = SkillService.objects.filter(student=stud)
    bookings = ServiceBooking.objects.filter(service__student=stud).order_by('-booking_date')
    
    context = {
        'services': services,
        'bookings': bookings,
        **get_notification_context(request.user)
    }
    return render(request, 'student/my_skills.html', context)

# Public / Employer Views for Skills

def service_list(request):
    services = SkillService.objects.filter(is_active=True, verification_status='verified')
    # Basic filtering
    category = request.GET.get('category')
    if category:
        services = services.filter(category=category)
    
    context = {'services': services}
    if request.user.is_authenticated:
        context.update(get_notification_context(request.user))
    return render(request, 'student/service_list.html', context)

def service_detail(request, service_id):
    service = get_object_or_404(SkillService, id=service_id)
    
    if request.method == 'POST':
        # Handle Booking
        requirements = request.POST.get('requirements')
        if not requirements:
            messages.error(request, "Please describe your requirements.")
        else:
            booking = ServiceBooking.objects.create(
                service=service,
                requester=request.user,
                requirements=requirements
            )
            messages.success(request, "Booking request sent successfully!")

            # Notifications
            Notification.objects.create(
                user=service.student.user,
                message=f"New skill request for '{service.title}' from {request.user.name}.",
                link='/student/my-skills/'
            )
            Notification.objects.create(
                user=request.user,
                message=f"Your request for '{service.title}' has been sent.",
                link=f"/student/services/{service.id}/"
            )
            return redirect('service_list')
    
    context = {'service': service}
    if request.user.is_authenticated:
        context.update(get_notification_context(request.user))
    return render(request, 'student/service_detail.html', context)

def edit_skill(request, service_id):
    service = get_object_or_404(SkillService, id=service_id)
    
    # Security check: Ensure the service belongs to the logged-in student
    if service.student.user.id != request.user.id:
        messages.error(request, "You are not authorized to edit this service.")
        return redirect('my_skills')

    if request.method == 'POST':
        form = SkillServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill updated successfully!")
            return redirect('my_skills')
    else:
        form = SkillServiceForm(instance=service)
    
    return render(request, 'student/add_skill.html', {'form': form, 'is_edit': True})

def manage_booking(request, booking_id, action):
    booking = get_object_or_404(ServiceBooking, id=booking_id)
    
    # Security check: Ensure the booking is for the logged-in student's service
    if booking.service.student.user.id != request.user.id:
        messages.error(request, "Unauthorized action.")
        return redirect('my_skills')
    
    from guest.models import Notification
    notification_message = None
    status_message = None
    
    if action == 'approve':
        booking.status = 'approved'
        status_message = "approved"
        notification_message = f"✅ Your request for '{booking.service.title}' has been APPROVED by {booking.service.student.student_name}."
        messages.success(request, "Booking request approved!")
    elif action == 'reject':
        booking.status = 'rejected'
        status_message = "rejected"
        notification_message = f"❌ Your request for '{booking.service.title}' has been REJECTED by {booking.service.student.student_name}."
        messages.error(request, "Booking request rejected.")
    elif action == 'complete':
        booking.status = 'completed'
        status_message = "completed"
        notification_message = f"✅ The service '{booking.service.title}' has been marked as COMPLETED by {booking.service.student.student_name}."
        messages.success(request, "Service marked as completed successfully!")
    elif action == 'revoke':
        booking.status = 'rejected'
        status_message = "revoked"
        notification_message = f"⚠️ The booking for '{booking.service.title}' has been REVOKED by {booking.service.student.student_name}."
        messages.warning(request, "Service booking has been revoked/stopped.")
    
    booking.save()

    # Notify requester about status update
    if notification_message:
        Notification.objects.create(
            user=booking.requester,
            message=notification_message,
            link='/student/services/'
        )
    
    return redirect('my_skills')
