from django.shortcuts import render, redirect
from guest.models import Employer
from guest.forms import EmployerForm, EmployerSignupForm, LoginForm, SignupForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

from employer.models import Jobposting
from student.models import Feedback, SkillService
# Force reload

def guest_index(request):
    jobs = Jobposting.objects.all().order_by('-posted_date')[:5]
    reviews = Feedback.objects.filter(rating__gte=4).order_by('-created_at')[:5]
    services = SkillService.objects.filter(is_active=True).order_by('-created_at')[:6]
    return render(request, 'guest/index.html', {'jobs': jobs, 'reviews': reviews, 'services': services})

def addemployer(request):
    if request.method == 'POST':
        form = EmployerSignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = EmployerSignupForm()
    return render(request, 'guest/addemployer.html', {'form': form})


def addstudent(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('guest_index')
    else:
        form = SignupForm()
    return render(request, 'guest/addstudent.html', {'form': form})


def signup(request):
    student_form = SignupForm(prefix="student")
    employer_form = EmployerSignupForm(prefix="employer")

    if request.method == 'POST':
        if 'student-submit' in request.POST:
            student_form = SignupForm(request.POST, request.FILES, prefix="student")
            employer_form = EmployerSignupForm(prefix="employer")
            if student_form.is_valid():
                student_form.save()
                messages.success(request, "Student registration successful! Your account is pending admin approval.")
                return redirect('login')
            else:
                messages.error(request, "Please correct the errors below.")
        elif 'employer-submit' in request.POST:
            employer_form = EmployerSignupForm(request.POST, prefix="employer")
            student_form = SignupForm(prefix="student")
            if employer_form.is_valid():
                employer_form.save()
                messages.success(request, "Employer registration successful! Your account is pending admin approval.")
                return redirect('login')
            else:
                messages.error(request, "Please correct the errors below.")

    return render(request, 'guest/signup.html', {
        'student_form': student_form,
        'employer_form': employer_form,
    })

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # authenticate using email (CustomUser has USERNAME_FIELD = "email")
            user = authenticate(request=request, username=email, password=password)

            if user is not None:
                # Check if user account is active
                if not user.is_active:
                    if user.role == 'employer':
                        messages.error(request, "Your employer account is pending admin approval. Please wait for verification.")
                    elif user.role == 'student':
                        messages.error(request, "Your student account is pending activation. Please contact support.")
                    else:
                        messages.error(request, "Your account is not active. Please contact support.")
                    return render(request, "guest/login.html", {"form": form})
                
                # Check if employer is verified
                if user.role == 'employer':
                    try:
                        employer = Employer.objects.get(user=user)
                        if not employer.verification_status:
                            messages.error(request, "Your account is pending admin approval. Please wait for verification.")
                            return render(request, "guest/login.html", {"form": form})
                    except Employer.DoesNotExist:
                        messages.error(request, "Employer profile not found.")
                        return render(request, "guest/login.html", {"form": form})
                
                login(request, user)
                messages.success(request, "Welcome Back!")

                # Redirect based on user role
                if user.role == 'admin':
                    return redirect("admin_index")
                elif user.role == 'employer':
                    return redirect("employer_index")
                elif user.role == 'student':
                    return redirect("student_index")
                else:
                    return redirect("guest_index")

            else:
                messages.error(request, "Invalid email or password.")
    else:
        form = LoginForm()

    return render(request, "guest/login.html", {"form": form})

def custom_logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')