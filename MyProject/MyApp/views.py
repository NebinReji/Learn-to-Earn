from django.shortcuts import render, redirect, get_object_or_404
from MyApp.models import District, Category, Subcategory
from MyApp.forms import CategoryForm, DistrictForm, SubcategoryForm
from guest.models import Employer, student, Feedback, Report
from django.contrib import messages
from django.utils import timezone
import csv
from django.http import HttpResponse

def index(request):
    total_students = student.objects.count()
    total_employers = Employer.objects.count()
    pending_verifications = Employer.objects.filter(verification_status=False).count()
    feedbacks = Feedback.objects.filter(status='new').count()
    
    context = {
        'total_students': total_students,
        'total_employers': total_employers,
        'pending_verifications': pending_verifications,
        'new_feedbacks': feedbacks,
    }
    return render(request, 'admin/index.html', context)

# ... (Existing District/Category Views remain unchanged)

# --- FEEDBACK MANAGEMENT ---
def view_feedback(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, 'admin/view_feedback.html', {'feedbacks': feedbacks})

def resolve_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback.status = 'resolved'
    feedback.save()
    messages.success(request, 'Feedback marked as resolved.')
    return redirect('view_feedback')

# --- REPORT GENERATION ---
def generate_report(request):
    if request.method == 'POST':
        report_type = request.POST.get('report_type')
        if report_type == 'users':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="users_report.csv"'
            writer = csv.writer(response)
            writer.writerow(['Name', 'Email', 'Role', 'Status'])
            # Fetch generic users or specific profiles? Using Student/Employer for detail
            for stud in student.objects.all():
                writer.writerow([stud.student_name, stud.email, 'Student', 'Active' if stud.user.is_active else 'Inactive'])
            for emp in Employer.objects.all():
                writer.writerow([emp.company_name, emp.email, 'Employer', 'Verified' if emp.verification_status else 'Pending'])
            return response
            
    return render(request, 'admin/generate_report.html')

# Verification Views (Ensure they exist and work)
def view_employers(request):
    employers = Employer.objects.all().order_by('-id')
    return render(request, 'admin/viewemployers.html', {'employers': employers})

def approve_employer(request, employer_id):
    try:
        employer = Employer.objects.get(id=employer_id)
        employer.verification_status = True
        employer.save()
        if employer.user:
            employer.user.is_active = True
            employer.user.save()
        messages.success(request, f'{employer.company_name} has been approved and activated!')
    except Employer.DoesNotExist:
        messages.error(request, 'Employer not found.')
    return redirect('view_employers')

def reject_employer(request, employer_id):
    try:
        employer = Employer.objects.get(id=employer_id)
        employer.verification_status = False
        employer.save()
        if employer.user:
            employer.user.is_active = False
            employer.user.save()
        messages.warning(request, f'{employer.company_name} has been rejected and deactivated.')
    except Employer.DoesNotExist:
        messages.error(request, 'Employer not found.')
    return redirect('view_employers')

# Student Verification Views
def view_students(request):
    students = student.objects.all().order_by('-id')
    return render(request, 'admin/viewstudents.html', {'students': students})

def approve_student(request, student_id):
    try:
        stud = student.objects.get(id=student_id)
        
        # Verify student profile
        stud.verification_status = True
        stud.save()

        # Activate user account
        if stud.user:
            stud.user.is_active = True
            stud.user.save()
        messages.success(request, f'{stud.student_name} has been approved and activated!')
    except student.DoesNotExist:
        messages.error(request, 'Student not found.')
    return redirect('view_students')

def reject_student(request, student_id):
    try:
        stud = student.objects.get(id=student_id)
        if stud.user:
            stud.user.is_active = False
            stud.user.save()
        messages.warning(request, f'{stud.student_name} has been rejected and deactivated.')
    except student.DoesNotExist:
        messages.error(request, 'Student not found.')
    return redirect('view_students')

# Skill Service Verification Views
from student.models import SkillService

def view_services(request):
    services = SkillService.objects.all().order_by('-created_at')
    return render(request, 'admin/view_services.html', {'services': services})

def approve_service(request, service_id):
    service = get_object_or_404(SkillService, id=service_id)
    service.verification_status = 'verified'
    service.save()
    messages.success(request, f'Service "{service.title}" has been verified.')
    return redirect('view_services')

def reject_service(request, service_id):
    service = get_object_or_404(SkillService, id=service_id)
    service.verification_status = 'rejected'
    service.save()
    messages.warning(request, f'Service "{service.title}" has been rejected.')
    return redirect('view_services')

# Include existing District/Category/Subcategory CRUD views below...
# (I will append the existing views logic here or assume user wants full replacement. 
# Better strategy: Replace the file content but keep the existing CRUD logic by re-writing it concisely)

def adddistrict(request):
    if request.method == 'POST':
        form = DistrictForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewdistrict')
    else:
        form = DistrictForm()
    return render(request, 'admin/adddistrict.html', {'form': form})

def viewdistrict(request):
    districts = District.objects.all()
    return render(request, 'admin/viewdistrict.html', {'districts': districts})

def editdistrict(request, district_id):
    district = get_object_or_404(District, district_id=district_id)
    if request.method == 'POST':
        form = DistrictForm(request.POST, instance=district)
        if form.is_valid():
            form.save()
            return redirect('viewdistrict')
    else:
        form = DistrictForm(instance=district)
    return render(request, 'admin/editdistrict.html', {'form': form, 'district': district})

def deletedistrict(request, district_id):
    district = get_object_or_404(District, district_id=district_id)
    district.delete()
    return redirect('viewdistrict')

def addcategory(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewcategory')
    else:
        form = CategoryForm()
    return render(request, 'admin/addcategory.html', {'form': form})

def viewcategory(request):
    categories = Category.objects.all()
    return render(request, 'admin/viewcategory.html', {'categories': categories})

def editcategory(request, category_id):
    category = get_object_or_404(Category, category_id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('viewcategory')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'admin/editcategory.html', {'form': form, 'category': category})

def deletecategory(request, category_id):
    category = get_object_or_404(Category, category_id=category_id)
    category.delete()
    return redirect('viewcategory')

def addsubcategory(request):
    if request.method == 'POST':
        form = SubcategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewsubcategory')
    else:
        form = SubcategoryForm()
    return render(request, 'admin/addsubcategory.html', {'form': form})

def viewsubcategory(request):
    subcategories = Subcategory.objects.all()
    return render(request, 'admin/viewsubcategory.html', {'subcategories': subcategories})

def editsubcategory(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, subcategory_id=subcategory_id)
    if request.method == 'POST':
        form = SubcategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect('viewsubcategory')
    else:
        form = SubcategoryForm(instance=subcategory)
    return render(request, 'admin/editsubcategory.html', {'form': form, 'subcategory': subcategory})

def deletesubcategory(request, subcategory_id):
    subcategory = get_object_or_404(Subcategory, subcategory_id=subcategory_id)
    subcategory.delete()
    return redirect('viewsubcategory')