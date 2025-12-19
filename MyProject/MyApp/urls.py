from django.urls import path
from MyApp import views

urlpatterns = [
    path('dashboard/', views.index, name='admin_index'),
    path('adddistrict/', views.adddistrict, name='adddistrict'),
    path('viewdistrict/', views.viewdistrict, name='viewdistrict'),
    path('editdistrict/<int:district_id>/', views.editdistrict, name='editdistrict'),
    path('deletedistrict/<int:district_id>/', views.deletedistrict, name='deletedistrict'),
    path('addcategory/', views.addcategory, name='addcategory'),
    path('viewcategory/', views.viewcategory, name='viewcategory'),
    path('editcategory/<int:category_id>/', views.editcategory, name='editcategory'),
    path('deletecategory/<int:category_id>/', views.deletecategory, name='deletecategory'),
    path('addsubcategory/', views.addsubcategory, name='addsubcategory'),
    path('viewsubcategory/', views.viewsubcategory, name='viewsubcategory'),
    path('editsubcategory/<int:subcategory_id>/', views.editsubcategory, name='editsubcategory'),
    path('deletesubcategory/<int:subcategory_id>/', views.deletesubcategory, name='deletesubcategory'),
    # Employer Verification
    path('employers/', views.view_employers, name='view_employers'),
    path('employers/approve/<int:employer_id>/', views.approve_employer, name='approve_employer'),
    path('employers/reject/<int:employer_id>/', views.reject_employer, name='reject_employer'),
    # Student Verification
    path('students/', views.view_students, name='view_students'),
    path('students/approve/<int:student_id>/', views.approve_student, name='approve_student'),
    path('students/reject/<int:student_id>/', views.reject_student, name='reject_student'),
]