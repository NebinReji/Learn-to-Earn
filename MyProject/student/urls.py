from django.urls import path
from student import views

urlpatterns = [
    path('', views.index, name='student_index'),
]
