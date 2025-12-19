from django.shortcuts import render, redirect
from guest.models import Employer
from employer.forms import JobPostingForm
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

