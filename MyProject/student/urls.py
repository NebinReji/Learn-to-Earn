from django.urls import path
from student import views

urlpatterns = [
    path('', views.index, name='student_index'),
    path('jobs/', views.view_jobs, name='student_view_jobs'),
    path('jobs/<int:job_id>/', views.job_detail, name='student_job_detail'),
    path('jobs/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('profile/', views.profile, name='student_profile'),
    path('notifications/', views.notifications, name='student_notifications'),
    path('my-applications/', views.my_applications, name='student_my_applications'),
]
