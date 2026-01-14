from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from employer.models import Jobposting
from guest.models import student
from student.models import Application
from student.forms import StudentProfileForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

@login_required
def profile(request):
    try:
        student_profile = student.objects.get(user=request.user)
    except student.DoesNotExist:
        messages.error(request, "Profile not found. Please contact admin.")
        return redirect('student_index')

    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated Successfully!")
            return redirect('student_profile')
    else:
        form = StudentProfileForm(instance=student_profile)

    return render(request, 'student/profile.html', {'form': form, 'student': student_profile})

@login_required
def index(request):
    return render(request, 'student/index.html')


def view_jobs(request):
    jobs = Jobposting.objects.select_related('employer').all()
    
    # Filter by Work Mode
    work_mode = request.GET.get('work_mode')
    if work_mode:
        jobs = jobs.filter(work_mode=work_mode)
        
    return render(request, 'student/viewjobs.html', {'jobs': jobs})


def job_detail(request, job_id):
    job = get_object_or_404(Jobposting.objects.select_related('employer'), id=job_id)
    application = None
    if request.user.is_authenticated and request.user.role == 'student':
        try:
            stud = student.objects.get(user=request.user)
            application = Application.objects.filter(student=stud, job=job).first()
        except:
            pass
            
    return render(request, 'student/job_detail.html', {'job': job, 'application': application})


@login_required
def apply_job(request, job_id):
    if request.user.role != 'student':
        messages.error(request, "Only registered students can apply for jobs.")
        return redirect('index') # Redirect to home or appropriate page

    try:
        stud = student.objects.get(user=request.user)
    except student.DoesNotExist:
        messages.error(request, "Student profile not found. Please complete your profile.")
        return redirect('index') # Redirect to profile creation or home
    
    # Check if already applied
    if Application.objects.filter(student=stud, job_id=job_id).exists():
        messages.warning(request, "You have already applied for this job.")
        return redirect('student_job_detail', job_id=job_id)
    
    # Create application
    # Create application
    Application.objects.create(student=stud, job_id=job_id)
    messages.success(request, "Application Sent Successfully!")
    
    return redirect('student_job_detail', job_id=job_id)
