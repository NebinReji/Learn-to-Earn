from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from guest.models import Employer
from employer.forms import JobPostingForm, EmployerProfileForm
from student.models import Application


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
    employer = Employer.objects.get(user_id=user_id)
    
    if request.method == 'POST':
        form = EmployerProfileForm(request.POST, request.FILES, instance=employer)
        if form.is_valid():
            form.save()
            return redirect('employer_profile')
    else:
        form = EmployerProfileForm(instance=employer)
        
    return render(request, 'employer/profile.html', {'form': form, 'employer': employer})


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
    
    if message:
        Notification.objects.create(user=application.student.user, message=message, link='/student/my-applications/')

    return redirect('view_applications')

