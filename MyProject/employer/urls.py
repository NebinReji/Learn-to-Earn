from django.urls import path
from employer import views

urlpatterns = [
    path('', views.index, name='employer_index'),
    path('addjob/', views.addjob, name='addjob'),
    path('viewjobs/', views.viewjobs, name='viewjobs'),
    path('editjob/<int:job_id>/', views.editjob, name='editjob'),
    path('deletejob/<int:job_id>/', views.deletejob, name='deletejob'),
    path('applications/', views.view_applications, name='view_applications'),
    path('profile/', views.profile, name='employer_profile'),
    path('setup-profile/', views.profile_setup, name='employer_profile_setup'),
    path('verification-pending/', views.verification_pending, name='employer_verification_pending'),
    path('application/<int:application_id>/status/<str:status>/', views.update_status, name='update_status'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('payment/<str:plan_type>/', views.payment_page, name='payment_page'),
    path('find-talent/', views.find_talent, name='employer_service_list'),
    path('find-talent/<int:service_id>/', views.service_detail, name='employer_service_detail'),
    path('student-profile/<int:student_id>/', views.view_student_profile, name='view_student_profile'),
]
