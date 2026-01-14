from django.shortcuts import render, redirect, get_object_or_404
from guest.models import Employer
from employer.models import SubscriptionPlan
from django.utils import timezone
from datetime import timedelta
from employer.forms import JobPostingForm, EmployerProfileForm
from student.models import Application
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    try:
        employer_profile = Employer.objects.get(user=request.user)
    except Employer.DoesNotExist:
        messages.error(request, "Employer profile not found.")
        return redirect('employer_index')

    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, request.FILES, instance=employer_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated Successfully!")
            return redirect('employer_profile')
    else:
        form = EmployerProfileForm(instance=employer_profile)

    return render(request, 'employer/profile.html', {'form': form, 'employer': employer_profile})
 


def index(request):
	return render(request, 'employer/index.html')


def addjob(request):
    user_id = request.user.id
    employer = Employer.objects.get(user_id=user_id)

    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = employer
            job.save()
            messages.success(request, "Job Posted Successfully!")
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
			messages.success(request, "Job Details Updated!")
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
		messages.success(request, "Job Deleted Successfully!")
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


def approve_application(request, application_id):
	user_id = request.user.id
	employer = Employer.objects.get(user_id=user_id)
	application = get_object_or_404(Application, id=application_id)
	if application.job.employer_id != employer.id:
		messages.error(request, 'You are not authorized to modify this application.')
		return redirect('view_applications')
	if request.method == 'POST':
		application.status = 'accepted'
		application.save()
		messages.success(request, "Application Approved!")
	return redirect('view_applications')


def reject_application(request, application_id):
	user_id = request.user.id
	employer = Employer.objects.get(user_id=user_id)
	application = get_object_or_404(Application, id=application_id)
	if application.job.employer_id != employer.id:
		messages.error(request, 'You are not authorized to modify this application.')
		return redirect('view_applications')
	if request.method == 'POST':
		application.status = 'rejected'
		application.save()
		messages.success(request, "Application Rejected!")
	return redirect('view_applications')


 

def subscriptions(request):
    user_id = request.user.id
    employer = Employer.objects.get(user_id=user_id)
    plans = SubscriptionPlan.objects.filter(emp=employer).order_by('-start_date')
    return render(request, 'employer/subscriptions.html', {'plans': plans})


def purchase_subscription(request):
    # Reduced logic here, mostly handled by payment_page
    return redirect('subscriptions')

def payment_page(request, plan_type):
    prices = {
        'sponsor': 199.00,
        'premium': 299.00
    }
    price = prices.get(plan_type, 0)
    return render(request, 'employer/payment.html', {'plan_name': plan_type, 'price': price})

def process_payment(request):
    if request.method == 'POST':
        user_id = request.user.id
        employer = Employer.objects.get(user_id=user_id)
        plan_name = request.POST.get('plan')
        
        # Determine price and features based on plan
        prices = {'sponsor': 199.00, 'premium': 299.00}
        features_map = {
            'sponsor': 'Priority listing, Email support, Verified badge',
            'premium': 'All features from Sponsor + Dedicated account manager, API access'
        }
        
        price = prices.get(plan_name, 0.00)
        features = features_map.get(plan_name, 'Basic features')
        
        SubscriptionPlan.objects.create(
            emp=employer,
            plan_name=plan_name,
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=30),
            price=price,
            features=features
        )
        messages.success(request, f"Subscription to {plan_name.title()} Activated!")
        return redirect('subscriptions')
    return redirect('subscriptions')

def shortlist_application(request, application_id):
    user_id = request.user.id
    employer = Employer.objects.get(user_id=user_id)
    application = get_object_or_404(Application, id=application_id)
    
    if application.job.employer_id != employer.id:
        messages.error(request, 'You are not authorized.')
        return redirect('view_applications')
        
    application.status = 'shortlisted'
    application.save()
    messages.success(request, "Candidate Shortlisted!")
    return redirect('view_applications')

def schedule_interview(request, application_id):
    if request.method != 'POST':
         return redirect('view_applications')
         
    user_id = request.user.id
    employer = Employer.objects.get(user_id=user_id)
    application = get_object_or_404(Application, id=application_id)
    
    if application.job.employer_id != employer.id:
        messages.error(request, 'You are not authorized.')
        return redirect('view_applications')
        
    interview_date = request.POST.get('interview_date')
    interview_mode = request.POST.get('interview_mode')
    interview_location = request.POST.get('interview_location')
    
    if interview_date and interview_mode:
        application.interview_date = interview_date
        application.interview_mode = interview_mode
        application.interview_location = interview_location
        # Keep status as shortlisted, or maybe 'interviewed'? Let's keep it simple or maybe update status?
        # User asked for shortlist -> interview. Status 'shortlisted' is fine, or we can add a flag. 
        # But let's assume Shortlisted is the bucket for interview candidates.
        application.save()
        messages.success(request, "Interview Scheduled!")
    else:
        messages.error(request, 'Missing interview details.')
        
    return redirect('view_applications')
