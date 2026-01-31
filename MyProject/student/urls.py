from django.urls import path
from student import views

urlpatterns = [
    path('', views.index, name='student_index'),
    path('jobs/', views.view_jobs, name='student_view_jobs'),
    path('jobs/<int:job_id>/', views.job_detail, name='student_job_detail'),
    path('jobs/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('profile/', views.profile, name='student_profile'),
    path('setup-profile/', views.profile_setup, name='student_profile_setup'),
    path('verification-pending/', views.verification_pending, name='student_verification_pending'),
    path('notifications/', views.notifications, name='student_notifications'),
    path('my-applications/', views.my_applications, name='student_my_applications'),
    
    # Skills & Services
    path('add-skill/', views.add_skill, name='add_skill'),
    path('my-skills/', views.my_skills, name='my_skills'),
    path('services/', views.service_list, name='service_list'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
    path('edit-skill/<int:service_id>/', views.edit_skill, name='edit_skill'),
    path('manage-booking/<int:booking_id>/<str:action>/', views.manage_booking, name='manage_booking'),
]
