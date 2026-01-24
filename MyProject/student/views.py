from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from employer.models import Jobposting
from guest.models import student
from student.models import Application, SkillService
from student.forms import StudentProfileForm


def index(request):
    try:
        stud = student.objects.get(user_id=request.user.id)
        
        # Redirect to Profile Completion if essential info is missing
        if not stud.institution_name or not stud.course_name:
            messages.info(request, "Please complete your profile to continue.")
            return redirect('complete_profile')
            
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
        
        # Dashboard Widgets
        from guest.models import Notification
        recent_notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')[:3]

        context = {
            'applications_count': applications_count,
            'my_skills_count': my_skills_count,
            'profile_completion': completion,
            'recent_jobs': recent_jobs,
            'available_skills': available_skills,
            'recent_applications': recent_applications,
            'recent_notifications': recent_notifications,
            'is_verified': stud.verification_status, # Pass verification status
        }
        return render(request, 'student/index.html', context)
    except student.DoesNotExist:
        return render(request, 'student/index.html')


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
    jobs = Jobposting.objects.select_related('employer').all()
    return render(request, 'student/viewjobs.html', {'jobs': jobs})


def job_detail(request, job_id):
    job = get_object_or_404(Jobposting.objects.select_related('employer'), id=job_id)
    
    # Check if applied
    is_applied = False
    if request.user.is_authenticated:
        try:
            stud = student.objects.get(user_id=request.user.id)
            is_applied = Application.objects.filter(student=stud, job_id=job_id).exists()
        except student.DoesNotExist:
            pass
            
    return render(request, 'student/job_detail.html', {'job': job, 'is_applied': is_applied})


def apply_job(request, job_id):
    user_id = request.user.id
    stud = student.objects.get(user_id=user_id)
    
    # Check if already applied
    if Application.objects.filter(student=stud, job_id=job_id).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('student_job_detail', job_id=job_id)
    
    # Create application
    Application.objects.create(student=stud, job_id=job_id)
    messages.success(request, "Successfully applied for the job!")
    
    return redirect('student_job_detail', job_id=job_id)
    return render(request, 'student/apply_job.html', {'job': job})

def profile(request):
    user_id = request.user.id
    stud = get_object_or_404(student, user_id=user_id)
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=stud)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('student_profile')
    else:
        form = StudentProfileForm(instance=stud)
        
    return render(request, 'student/profile.html', {'form': form, 'student': stud})

def notifications(request):
    from guest.models import Notification
    notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')
    
    # Mark as read
    notifications.update(is_read=True)
    
    return render(request, 'student/notifications.html', {'notifications': notifications})


def my_applications(request):
    user_id = request.user.id
    stud = get_object_or_404(student, user_id=user_id)
    applications = Application.objects.filter(student=stud).select_related('job', 'job__employer').order_by('-applied_date')
    return render(request, 'student/my_applications.html', {'applications': applications})

from student.forms import FeedbackForm
from student.models import Feedback

def review_employer(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    
    # Verify student owns the application
    if application.student.user != request.user:
        messages.error(request, "Unauthorized")
        return redirect('student_my_applications')
        
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.application = application
            feedback.reviewer_role = 'student'
            feedback.save()
            messages.success(request, "Feedback submitted successfully!")
            return redirect('student_my_applications')
    else:
        form = FeedbackForm()
    
    return render(request, 'student/review_employer.html', {'form': form, 'application': application})

# -------------------- Skills & Services Views --------------------

from .models import SkillService, ServiceBooking
from .forms import SkillServiceForm

def add_skill(request):
    user_id = request.user.id
    stud = get_object_or_404(student, user_id=user_id)
    
    if request.method == 'POST':
        form = SkillServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.student = stud
            service.save()
            messages.success(request, "Skill Service added successfully!")
            return redirect('my_skills')
    else:
        form = SkillServiceForm()
        
    return render(request, 'student/add_skill.html', {'form': form})

def my_skills(request):
    user_id = request.user.id
    stud = get_object_or_404(student, user_id=user_id)
    services = SkillService.objects.filter(student=stud)
    bookings = ServiceBooking.objects.filter(service__student=stud).order_by('-booking_date')
    
    return render(request, 'student/my_skills.html', {'services': services, 'bookings': bookings})

# Public / Employer Views for Skills

def service_list(request):
    services = SkillService.objects.filter(is_active=True, verification_status='verified')
    # Basic filtering
    category = request.GET.get('category')
    if category:
        services = services.filter(category=category)
        
    return render(request, 'student/service_list.html', {'services': services})

def service_detail(request, service_id):
    service = get_object_or_404(SkillService, id=service_id)
    
    if request.method == 'POST':
        # Handle Booking
        requirements = request.POST.get('requirements')
        if not requirements:
            messages.error(request, "Please describe your requirements.")
        else:
            ServiceBooking.objects.create(
                service=service,
                requester=request.user,
                requirements=requirements
            )
            messages.success(request, "Booking request sent successfully!")
            return redirect('service_list')
            
    return render(request, 'student/service_detail.html', {'service': service})

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
        
    if action == 'approve':
        booking.status = 'approved'
        messages.success(request, "Booking request approved!")
    elif action == 'reject':
        booking.status = 'rejected'
        messages.error(request, "Booking request rejected.")
    elif action == 'complete':
        booking.status = 'completed'
        messages.success(request, "Service marked as completed successfully!")
    elif action == 'revoke':
        booking.status = 'rejected'
        messages.warning(request, "Service booking has been revoked/stopped.")
    
    booking.save()
    return redirect('my_skills')
