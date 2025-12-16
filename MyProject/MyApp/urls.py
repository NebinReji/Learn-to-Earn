from django.urls import path
from MyApp import views


urlpatterns = [
    path('', views.index, name='index'),
    path('adddistrict/', views.adddistrict, name='adddistrict'),
    path('viewdistrict/', views.viewdistrict, name='viewdistrict'),
    path('editdistrict/<int:district_id>/', views.editdistrict, name='editdistrict'),
    path('deletedistrict/<int:district_id>/', views.deletedistrict, name='deletedistrict'),
    path('addcategory/', views.addcategory, name='addcategory'),
    path('viewcategory/', views.viewcategory, name='viewcategory'),
    path('editcategory/<int:category_id>/', views.editcategory, name='editcategory'),
    path('deletecategory/<int:category_id>/', views.deletecategory, name='deletecategory'),
    path('addsubcategory/', views.addsubcategory, name='addsubcategory'),
    path('viewsubcategory/', views.viewsubcategory, name='viewsubcategory'),
    path('editsubcategory/<int:subcategory_id>/', views.editsubcategory, name='editsubcategory'),
    path('deletesubcategory/<int:subcategory_id>/', views.deletesubcategory, name='deletesubcategory'),
    path('viewsubcategory/', views.viewsubcategory, name='viewsubcategory'),
]