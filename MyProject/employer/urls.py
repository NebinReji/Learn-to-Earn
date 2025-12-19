from django.urls import path
from employer import views

urlpatterns = [
    path('', views.index, name='employer_index'),
    path('addjob/', views.addjob, name='addjob'),
    path('viewjobs/', views.viewjobs, name='viewjobs'),
    path('editjob/<int:job_id>/', views.editjob, name='editjob'),
    path('deletejob/<int:job_id>/', views.deletejob, name='deletejob'),
    path('applications/', views.view_applications, name='view_applications'),
]
