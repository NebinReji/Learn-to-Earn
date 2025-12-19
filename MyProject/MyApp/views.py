from django.shortcuts import render, redirect
from MyApp.models import District, Category, Subcategory
from MyApp.forms import CategoryForm, DistrictForm, SubcategoryForm
from guest.models import Employer, student
from django.contrib import messages

def index(request):
    return render(request, 'admin/index.html')

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
    try:
        district = District.objects.get(district_id=district_id)
    except District.DoesNotExist:
        return redirect('viewdistrict')
    
    if request.method == 'POST':
        form = DistrictForm(request.POST, instance=district)
        if form.is_valid():
            form.save()
            return redirect('viewdistrict')
    else:
        form = DistrictForm(instance=district)
    return render(request, 'admin/editdistrict.html', {'form': form, 'district': district})
def deletedistrict(request, district_id):
    try:
        district = District.objects.get(district_id=district_id)
        district.delete()
    except District.DoesNotExist:
        pass
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
    try:
        category = Category.objects.get(category_id=category_id)
    except Category.DoesNotExist:
        return redirect('viewcategory')
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('viewcategory')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'admin/editcategory.html', {'form': form, 'category': category})

def deletecategory(request, category_id):
    try:
        category = Category.objects.get(category_id=category_id)
        category.delete()
    except Category.DoesNotExist:
        pass
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
    try:
        subcategory = Subcategory.objects.get(subcategory_id=subcategory_id)
    except Subcategory.DoesNotExist:
        return redirect('viewsubcategory')
    
    if request.method == 'POST':
        form = SubcategoryForm(request.POST, instance=subcategory)
        if form.is_valid():
            form.save()
            return redirect('viewsubcategory')
    else:
        form = SubcategoryForm(instance=subcategory)
    return render(request, 'admin/editsubcategory.html', {'form': form, 'subcategory': subcategory})

def deletesubcategory(request, subcategory_id):
    try:
        subcategory = Subcategory.objects.get(subcategory_id=subcategory_id)
        subcategory.delete()
    except Subcategory.DoesNotExist:
        pass
    return redirect('viewsubcategory')

# Employer Verification Views
def view_employers(request):
    employers = Employer.objects.all().order_by('-id')
    return render(request, 'admin/viewemployers.html', {'employers': employers})

def approve_employer(request, employer_id):
    try:
        employer = Employer.objects.get(id=employer_id)
        employer.verification_status = True
        employer.save()
        # Activate the user account
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
        # Deactivate the user account
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
        # Activate the user account
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
        # Deactivate the user account
        if stud.user:
            stud.user.is_active = False
            stud.user.save()
        messages.warning(request, f'{stud.student_name} has been rejected and deactivated.')
    except student.DoesNotExist:
        messages.error(request, 'Student not found.')
    return redirect('view_students')