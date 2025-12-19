from django.urls import path
from django.contrib.auth.views import LogoutView
from guest import views

urlpatterns = [
    path('', views.guest_index, name='guest_index'),
    path('signup/', views.signup, name='signup'),
    path('addemployer/', views.addemployer, name='addemployer'),
    path('addstudent/', views.addstudent, name='addstudent'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]