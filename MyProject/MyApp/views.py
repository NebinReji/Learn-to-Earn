from django.shortcuts import render, redirect
from MyApp.models import District, Category, Subcategory
from MyApp.forms import CategoryForm, DistrictForm, SubcategoryForm

def index(request):
    return render(request, 'index.html')

def adddistrict(request):
    if request.method == 'POST':
        form = DistrictForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewdistrict')
    else:
        form = DistrictForm()
    return render(request, 'adddistrict.html', {'form': form})

def viewdistrict(request):
    districts = District.objects.all()
    return render(request, 'viewdistrict.html', {'districts': districts})

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
    return render(request, 'editdistrict.html', {'form': form, 'district': district})
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
    return render(request, 'addcategory.html', {'form': form})
def viewcategory(request):
    categories = Category.objects.all()
    return render(request, 'viewcategory.html', {'categories': categories})

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
    return render(request, 'editcategory.html', {'form': form, 'category': category})

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
    return render(request, 'addsubcategory.html', {'form': form})

def viewsubcategory(request):
    subcategories = Subcategory.objects.all()
    return render(request, 'viewsubcategory.html', {'subcategories': subcategories})

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
    return render(request, 'editsubcategory.html', {'form': form, 'subcategory': subcategory})

def deletesubcategory(request, subcategory_id):
    try:
        subcategory = Subcategory.objects.get(subcategory_id=subcategory_id)
        subcategory.delete()
    except Subcategory.DoesNotExist:
        pass
    return redirect('viewsubcategory')
