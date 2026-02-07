from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from guest.models import Employer, student, Notification
from employer.models import Subscription
from employer.forms import JobPostingForm, EmployerProfileForm, EmployerProfileSetupForm
from student.models import Application


# Helper function to get notification data for context
def get_notification_context(user):
    """Returns notification data for navbar"""
    return {
        'recent_notifications': Notification.objects.filter(user=user).order_by('-timestamp')[:5],
        'unread_notifications_count': Notification.objects.filter(user=user, is_read=False).count()
    }



def index(request):
    try:
        employer = Employer.objects.get(user_id=request.user.id)
        
        if not employer.is_profile_complete():
            return redirect('employer_profile_setup')

        if not employer.verification_status:
            return redirect('employer_verification_pending')

        jobs_count = employer.job_postings.count()
        total_applications_count = Application.objects.filter(job__employer=employer).count()
        shortlisted_count = Application.objects.filter(job__employer=employer, status='shortlisted').count()
        recent_applications = Application.objects.filter(job__employer=employer).select_related('student__user', 'job').order_by('-id')[:5]

        # Fetch Notifications
        notification_context = get_notification_context(request.user)

        # Subscription status for dashboard banner
        subscription_status = employer.get_subscription_status()
        trial_info = {
            'is_active': subscription_status['is_in_trial'],
            'days_remaining': subscription_status['days_remaining'],
            'trial_expires_at': subscription_status['trial_expires_at'],
            'is_expiring_soon': 0 < subscription_status['days_remaining'] <= 3,
        }
        
        context = {
            'jobs_count': jobs_count,
            'total_applications_count': total_applications_count,
            'shortlisted_count': shortlisted_count,
            'recent_applications': recent_applications,
            'subscription_status': subscription_status,
            'trial_info': trial_info,
            **notification_context,  # Add notification data
        }
        return render(request, 'employer/index.html', context)
    except Employer.DoesNotExist:
        return redirect('employer_profile_setup')


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

    subscription_status = employer.get_subscription_status()
    if not subscription_status['can_post_jobs']:
        messages.warning(request, "Your trial has ended. Please subscribe to continue posting jobs.")
        return redirect('subscriptions')

    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = employer
            job.save()
            messages.success(request, "Job posted successfully!")
            
            # Send notification to employer
            from guest.models import Notification
            Notification.objects.create(
                user=request.user,
                message=f"✅ Your job '{job.job_title}' has been posted successfully and is now visible to students.",
                link='/employer/viewjobs/'
            )
            
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


def shortlisted_candidates(request):
    user_id = request.user.id
    employer = Employer.objects.get(user_id=user_id)

    jobs = employer.job_postings.all()
    applications = Application.objects.filter(
        job__in=jobs,
        status='shortlisted'
    ).select_related('student__user', 'job')

    return render(request, 'employer/shortlisted_candidates.html', {'applications': applications})



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
    if status == 'reviewed':
        message = f"📋 Your application for {application.job.job_title} at {application.job.employer.company_name} has been reviewed."
    elif status == 'shortlisted':
        message = f"🎉 Congratulations! You have been shortlisted for the position of {application.job.job_title} at {application.job.employer.company_name}."
    elif status == 'accepted':
        message = f"✅ Great news! Your application for {application.job.job_title} has been ACCEPTED by {application.job.employer.company_name}. Get ready to start!"
    elif status == 'rejected':
        message = f"❌ Update on your application: {application.job.employer.company_name} has decided not to proceed with your application for {application.job.job_title}. Better luck next time!"
    elif status == 'completed':
        message = f"✨ Congratulations! Your job {application.job.job_title} has been marked as COMPLETED by {application.job.employer.company_name}. Please leave your feedback!"
    
    if message:
        Notification.objects.create(user=application.student.user, message=message, link='/student/my-applications/')

    return redirect('view_applications')


from student.forms import FeedbackForm
from student.models import Feedback

def mark_job_completed(request, application_id):
    """Mark a job as completed - Employer can do this"""
    application = get_object_or_404(Application, id=application_id)
    
    # Verify employer owns the job
    if application.job.employer.user != request.user:
        messages.error(request, "Unauthorized")
        return redirect('view_applications')
    
    # Only allow marking as completed if status is 'accepted'
    if application.status != 'accepted':
        messages.error(request, "Job must be in 'accepted' status to mark as completed.")
        return redirect('view_applications')
    
    application.status = 'completed'
    application.save()
    
    # Create Notification
    from guest.models import Notification
    message = f"Great news! Your job '{application.job.job_title}' has been marked as COMPLETED by {application.job.employer.company_name}. Please leave feedback to help us improve."
    Notification.objects.create(
        user=application.student.user,
        message=message,
        link=f'/student/my-applications/'
    )
    
    messages.success(request, "Job marked as completed! Student will be notified.")
    return redirect('view_applications')


def review_student(request, application_id):
    """Employer provides feedback about the student"""
    application = get_object_or_404(Application, id=application_id)
    
    # Verify employer owns the job
    if application.job.employer.user != request.user:
        messages.error(request, "Unauthorized")
        return redirect('view_applications')
    
    # Check if feedback already exists from employer
    existing_feedback = Feedback.objects.filter(
        application=application,
        reviewer_role='employer'
    ).first()
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=existing_feedback)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.application = application
            feedback.reviewer_role = 'employer'
            feedback.save()
            messages.success(request, "Feedback submitted successfully!")
            
            # Send notification to student
            from guest.models import Notification
            if existing_feedback:
                # Updated feedback
                notification_message = f"{application.job.employer.company_name} has updated their feedback for the '{application.job.job_title}' job."
            else:
                # New feedback
                notification_message = f"{application.job.employer.company_name} has shared feedback for your work on '{application.job.job_title}' (Rating: {feedback.rating}⭐)."
            
            Notification.objects.create(
                user=application.student.user,
                message=notification_message,
                link=f'/student/my-applications/{application.id}/feedback/'
            )
            
            return redirect('view_applications')
    else:
        form = FeedbackForm(instance=existing_feedback)
    
    context = {
        'form': form,
        'application': application,
        'existing_feedback': existing_feedback
    }
    return render(request, 'employer/review_student.html', context)


def subscriptions(request):
    from django.utils import timezone
    from employer.models import Subscription
    
    employer = request.user.employer_profile
    
    # Get or create free trial for new employers
    if not employer.subscriptions.exists():
        employer.init_free_trial()
    
    # Get subscription status
    subscription_status = employer.get_subscription_status()
    
    # Get subscription history
    subscriptions = employer.subscriptions.all().order_by('-start_date')
    
    # Calculate trial information
    trial_info = {
        'is_active': subscription_status['is_in_trial'],
        'days_remaining': subscription_status['days_remaining'],
        'trial_expires_at': subscription_status['trial_expires_at'],
        'is_expiring_soon': False,
        'expires_in_days': subscription_status['days_remaining']
    }
    
    # Check if trial is expiring soon (3 days or less)
    if 0 < subscription_status['days_remaining'] <= 3:
        trial_info['is_expiring_soon'] = True
    
    context = {
        'subscription_status': subscription_status,
        'trial_info': trial_info,
        'subscriptions': subscriptions,
        'current_subscription': subscriptions.first() if subscriptions.exists() else None,
        'today': timezone.now().date(),
    }
    
    context.update(get_notification_context(request.user))
    return render(request, 'employer/subscriptions.html', context)

def payment_page(request, plan_type):
    # Plan pricing and details
    plans = {
        'sponsor': {
            'name': 'Sponsor',
            'price': 199,
            'duration': 'month',
            'features': [
                'Priority placement in listings',
                'Boosted reach for all jobs',
                'Email + Mobile alerts to candidates',
                'Analytics Dashboard',
            ]
        },
        'premium': {
            'name': 'Premium',
            'price': 299,
            'duration': 'month',
            'features': [
                'Unlimited job postings',
                'Top-tier placement & branding',
                'Dedicated support manager',
                'Access to resume database',
            ]
        },
        'basic': {
            'name': 'Basic',
            'price': 0,
            'duration': 'month',
            'features': [
                'Post up to 2 jobs/month',
                'Basic listing visibility',
                'Candidate management',
            ]
        }
    }
    
    if plan_type not in plans:
        messages.error(request, "Invalid plan selection. Please choose a valid plan.")
        return redirect('subscriptions')

    plan_data = plans[plan_type]
    context = {
        'plan_type': plan_type,
        'plan_name': plan_data['name'],
        'price': plan_data['price'],
        'duration': plan_data['duration'],
        'features': plan_data['features'],
    }
    return render(request, 'employer/payment.html', context)


def process_payment(request):
    """Process payment and create subscription."""
    from django.contrib import messages
    from django.utils import timezone
    from datetime import timedelta
    
    if request.method == 'POST':
        try:
            plan_type = request.POST.get('plan')
            employer = request.user.employer_profile
            
            # Plan pricing and label mapping
            plan_config = {
                'sponsor': {'price': 199.00, 'plan_name': 'sponsor', 'label': 'Sponsor'},
                'premium': {'price': 299.00, 'plan_name': 'premium', 'label': 'Premium'},
                'basic': {'price': 0.00, 'plan_name': 'basic', 'label': 'Basic'},
            }
            
            if plan_type not in plan_config:
                messages.error(request, "Invalid plan selection. Please try again.")
                return redirect('subscriptions')

            config = plan_config[plan_type]
            amount = config['price']
            plan_name = config['plan_name']
            label = config['label']
            
            # Deactivate previous active subscriptions
            Subscription.objects.filter(employer=employer, is_active=True).update(is_active=False)
            
            # Create new subscription
            end_date = timezone.now().date() + timedelta(days=30)
            
            subscription = Subscription.objects.create(
                employer=employer,
                plan_name=plan_name,
                amount=amount,
                is_active=True,
                end_date=end_date,
                is_free_trial=False,
            )
            
            messages.success(request, f'✅ Payment successful! You are now on the {label} plan.')
            return redirect('subscriptions')
            
        except Exception as e:
            messages.error(request, f'❌ Payment failed: {str(e)}')
            return redirect('subscriptions')
    
    return redirect('subscriptions')


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

def view_applied_student(request, application_id):
    """View student profile with feedback from this application"""
    application = get_object_or_404(Application, id=application_id)
    
    # Verify employer owns the job
    if application.job.employer.user != request.user:
        messages.error(request, "Unauthorized")
        return redirect('view_applications')
    
    # Get all feedback for this application
    student_feedbacks = Feedback.objects.filter(
        application=application,
        reviewer_role='student'
    )
    employer_feedbacks = Feedback.objects.filter(
        application=application,
        reviewer_role='employer'
    )
    
    context = {
        'application': application,
        'student': application.student,
        'student_feedbacks': student_feedbacks,
        'employer_feedbacks': employer_feedbacks,
    }
    return render(request, 'employer/view_applied_student.html', context)


def view_student_profile(request, student_id):
    student_obj = get_object_or_404(student, id=student_id)
    # Check if student has applied to any of employer's jobs for security context (optional but good practice)
    # For now, allow viewing if they have applied, or if checking talent.
    
    # Get feedback for this student if there are any applications
    from student.models import Application as StudentApplication
    applications = StudentApplication.objects.filter(
        student=student_obj,
        job__employer__user=request.user
    )
    
    feedbacks = Feedback.objects.filter(
        application__in=applications,
        reviewer_role='student'  # Student's feedback about employer
    )
    
    return render(request, 'employer/student_profile.html', {
        'student': student_obj,
        'feedbacks': feedbacks
    })
