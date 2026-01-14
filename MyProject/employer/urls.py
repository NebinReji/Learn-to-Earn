from django.urls import path
from employer import views

urlpatterns = [
    path('', views.index, name='employer_index'),
    path('addjob/', views.addjob, name='addjob'),
    path('viewjobs/', views.viewjobs, name='viewjobs'),
    path('editjob/<int:job_id>/', views.editjob, name='editjob'),
    path('deletejob/<int:job_id>/', views.deletejob, name='deletejob'),
    path('applications/', views.view_applications, name='view_applications'),
    path('applications/<int:application_id>/approve/', views.approve_application, name='approve_application'),
    path('applications/<int:application_id>/reject/', views.reject_application, name='reject_application'),
    path('applications/<int:application_id>/shortlist/', views.shortlist_application, name='shortlist_application'),
    path('applications/<int:application_id>/schedule/', views.schedule_interview, name='schedule_interview'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('payment/<str:plan_type>/', views.payment_page, name='payment_page'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('profile/', views.profile, name='employer_profile'),
]
