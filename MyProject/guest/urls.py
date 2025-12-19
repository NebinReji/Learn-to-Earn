from django.urls import path
from guest import views

urlpatterns = [
    path('', views.guest_index, name='guest_index'),
    path('signup/', views.signup, name='signup'),
    path('addemployer/', views.addemployer, name='addemployer'),
    path('addstudent/', views.addstudent, name='addstudent'),
    path('login/', views.login_view, name='login'),
]