from django.urls import path
from employer import views

urlpatterns = [
    path('', views.index, name='employer_index'),
]
