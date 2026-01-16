from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from employer.models import Jobposting
from guest.models import student
from student.models import Application
from student.forms import StudentProfileForm


def index(request):
    return render(request, 'student/index.html')


def view_jobs(request):
    jobs = Jobposting.objects.select_related('employer').all()
    return render(request, 'student/viewjobs.html', {'jobs': jobs})


def job_detail(request, job_id):
    job = get_object_or_404(Jobposting.objects.select_related('employer'), id=job_id)
    return render(request, 'student/job_detail.html', {'job': job})


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
