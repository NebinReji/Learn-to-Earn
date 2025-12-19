from django.shortcuts import render, redirect
from employer.forms import JobPostingForm


def index(request):
	return render(request, 'employer/index.html')


def addjob(request):
	if request.method == 'POST':
		form = JobPostingForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('employer_index')
	else:
		form = JobPostingForm()
	return render(request, 'employer/addjob.html', {'form': form})
