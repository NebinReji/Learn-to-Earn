from django.urls import path
from guest import views

urlpatterns = [
    path('', views.guest_index, name='guest_index'),
    path('addemployer/', views.addemployer, name='addemployer'),
    path('viewemployer/', views.viewemployer, name='viewemployer'),
    path('editemployer/<int:employer_id>/', views.editemployer, name='editemployer'),
    path('deleteemployer/<int:employer_id>/', views.deleteemployer, name='deleteemployer'),
    path('addjob/', views.addjob, name='addjob'),
]