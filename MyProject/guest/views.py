from django.shortcuts import render, redirect
from guest.models import Employer
from guest.forms import EmployerForm, JobPostingForm

def guest_index(request):
    return render(request, 'guest/index.html')

def addemployer(request):
    if request.method == 'POST':
        form = EmployerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewemployer')
    else:
        form = EmployerForm()
    return render(request, 'guest/addemployer.html', {'form': form})

def viewemployer(request):
    employers = Employer.objects.all()
    return render(request, 'guest/viewemployer.html', {'employers': employers})

def editemployer(request, employer_id):
    try:
        employer = Employer.objects.get(employer_id=employer_id)
    except Employer.DoesNotExist:
        return redirect('viewemployer')
    
    if request.method == 'POST':
        form = EmployerForm(request.POST, instance=employer)
        if form.is_valid():
            form.save()
            return redirect('viewemployer')
    else:
        form = EmployerForm(instance=employer)
    return render(request, 'guest/editemployer.html', {'form': form, 'employer': employer})

def deleteemployer(request, employer_id):
    try:
        employer = Employer.objects.get(employer_id=employer_id)
        employer.delete()
    except Employer.DoesNotExist:
        pass
    return redirect('viewemployer')

def addjob(request):
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewjobpostings')
    else:
        form = JobPostingForm()
    return render(request, 'guest/addjob.html', {'form': form})