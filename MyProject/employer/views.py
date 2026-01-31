from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from guest.models import Employer, student
from employer.forms import JobPostingForm, EmployerProfileForm, EmployerProfileSetupForm
from student.models import Application


def index(request):
    try:
        employer = Employer.objects.get(user_id=request.user.id)
        jobs_count = employer.job_postings.count()
        total_applications_count = Application.objects.filter(job__employer=employer).count()
        shortlisted_count = Application.objects.filter(job__employer=employer, status='shortlisted').count()
        recent_applications = Application.objects.filter(job__employer=employer).select_related('student__user', 'job').order_by('-id')[:5]

        # Fetch Notifications (last 5)
        from guest.models import Notification
        recent_notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')[:5]

        context = {
            'jobs_count': jobs_count,
            'total_applications_count': total_applications_count,
            'shortlisted_count': shortlisted_count,
            'recent_applications': recent_applications,
            'recent_notifications': recent_notifications,
        }
        return render(request, 'employer/index.html', context)
    except Employer.DoesNotExist:
        return render(request, 'employer/index.html')


def addjob(request):
    user_id = request.user.id
    try:
        employer = Employer.objects.get(user_id=user_id)
    except Employer.DoesNotExist:
        messages.error(request, "Company profile not found. Please complete setup.")
        return redirect('employer_profile_setup')

    # Check if profile is complete
    if not employer.is_profile_complete():
        messages.error(request, "Please complete your company profile before posting jobs.")
        return redirect('employer_profile_setup')

    if not employer.verification_status:
        messages.warning(request, "Your company profile is under verification. You can post jobs once verified.")
        return redirect('employer_verification_pending')

    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = employer
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect('employer_index')
    else:
        form = JobPostingForm()

    return render(request, 'employer/addjob.html', {'form': form})



def viewjobs(request):
    user_id = request.user.id
    employer = Employer.objects.get(user_id=user_id)
    jobs = employer.job_postings.all()
    return render(request, 'employer/viewjobs.html', {'jobs': jobs})

def editjob(request, job_id):
    user_id = request.user.id
    employer = Employer.objects.get(user_id=user_id)
    
    try:
        job = employer.job_postings.get(id=job_id)
    except:
        return redirect('viewjobs')
    
    if request.method == 'POST':
        form = JobPostingForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, "Job updated successfully!")
            return redirect('viewjobs')
    else:
        form = JobPostingForm(instance=job)
    
    return render(request, 'employer/editjob.html', {'form': form, 'job': job})

def deletejob(request, job_id):
    user_id = request.user.id
    employer = Employer.objects.get(user_id=user_id)
    
    try:
        job = employer.job_postings.get(id=job_id)
        job.delete()
    except:
        pass
    
    return redirect('viewjobs')


def view_applications(request):
    user_id = request.user.id
    employer = Employer.objects.get(user_id=user_id)
    
    # Get all jobs posted by this employer
    jobs = employer.job_postings.all()
    
    # Get all applications for those jobs
    applications = Application.objects.filter(job__in=jobs).select_related('student__user', 'job')
    
    
    return render(request, 'employer/view_applications.html', {'applications': applications})



def profile(request):
    user_id = request.user.id
    # Auto-create if missing
    employer, created = Employer.objects.get_or_create(
        user_id=user_id,
        defaults={
            'company_name': request.user.name or "Company Name",
            'contact_person': request.user.name or "Contact Person",
            'email': request.user.email,
            'phone': '',
        }
    )
    
    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, request.FILES, instance=employer)
        if form.is_valid():
            form.save()
            return redirect('employer_profile')
    else:
        form = EmployerProfileForm(instance=employer)
        
    return render(request, 'employer/profile.html', {'form': form, 'employer': employer})

def profile_setup(request):
    user_id = request.user.id
    # Auto-create if missing
    employer, created = Employer.objects.get_or_create(
        user_id=user_id,
        defaults={
            'company_name': request.user.name or "Company Name",
            'contact_person': request.user.name or "Contact Person",
            'email': request.user.email,
            'phone': '',
        }
    )
    
    if request.method == 'POST':
        form = EmployerProfileSetupForm(request.POST, request.FILES, instance=employer)
        if form.is_valid():
            employer = form.save(commit=False)
            employer.verification_status = False # Ensure it remains False until Admin approves
            employer.save()
            messages.info(request, "Company profile setup complete! Your account is pending Admin verification.")
            return redirect('employer_verification_pending')
    else:
        form = EmployerProfileSetupForm(instance=employer)
        
    return render(request, 'employer/profile_setup.html', {'form': form})


def verification_pending(request):
    return render(request, 'employer/verification_pending.html')


def update_status(request, application_id, status):
    application = get_object_or_404(Application, id=application_id)
    
    # Verify employer owns the job
    if application.job.employer.user != request.user:
        return redirect('view_applications')

    application.status = status
    application.save()

    # Create Notification
    from guest.models import Notification
    message = ""
    if status == 'shortlisted':
        message = f"Congratulations! You have been shortlisted for the position of {application.job.job_title} at {application.job.employer.company_name}."
    elif status == 'accepted':
        message = f"Great news! Your application for {application.job.job_title} has been ACCEPTED by {application.job.employer.company_name}."
    elif status == 'rejected':
        message = f"Update on your application: {application.job.employer.company_name} has decided not to proceed with your application for {application.job.job_title}."
    elif status == 'completed':
        message = f"Congratulations! Your job {application.job.job_title} has been marked as COMPLETED by {application.job.employer.company_name}. Please check your application status and leave a review."
    
    if message:
        Notification.objects.create(user=application.student.user, message=message, link='/student/my-applications/')

    return redirect('view_applications')


from student.forms import FeedbackForm
from student.models import Feedback

def review_student(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    
    # Verify employer owns the job
    if application.job.employer.user != request.user:
        messages.error(request, "Unauthorized")
        return redirect('view_applications')
        
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.application = application
            feedback.reviewer_role = 'employer'
            feedback.save()
            messages.success(request, "Feedback submitted successfully!")
            return redirect('view_applications')
    else:
        form = FeedbackForm()
    
    return render(request, 'employer/review_student.html', {'form': form, 'application': application})

    return render(request, 'employer/review_student.html', {'form': form, 'application': application})


def subscriptions(request):
    plan_type = request.GET.get('plan', 'monthly')  # Default to monthly if not specified
    plans = [] # Placeholder for actual DB plans if needed
    return render(request, 'employer/subscriptions.html', {'plan_type': plan_type, 'plans': plans})

def payment_page(request, plan_type):
    return render(request, 'employer/payment.html', {'plan_type': plan_type})


from student.models import SkillService

def find_talent(request):
    services = SkillService.objects.filter(is_active=True, verification_status='verified')
    category = request.GET.get('category')
    if category:
        services = services.filter(category=category)
    return render(request, 'employer/service_list.html', {'services': services})

def service_detail(request, service_id):
    service = get_object_or_404(SkillService, id=service_id)
    return render(request, 'employer/service_detail.html', {'service': service})

def view_student_profile(request, student_id):
    student_obj = get_object_or_404(student, id=student_id)
    # Check if student has applied to any of employer's jobs for security context (optional but good practice)
    # For now, allow viewing if they have applied, or if checking talent.
    
    return render(request, 'employer/student_profile.html', {'student': student_obj})
