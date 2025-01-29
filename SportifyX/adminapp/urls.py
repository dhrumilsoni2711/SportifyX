from django.contrib.auth import views as auth_views
from django.urls import path
from adminapp import views


urlpatterns = [
    path('adminindex/', views.adminindex, name='adminindex'),
    path('formhorizontal/', views.formhorizontal, name='formhorizontal'),
    path('usertable/', views.usertable, name='usertable'),
    path('venuetable/', views.venuetable, name='venuetable'),
    path('addvenue/', views.addvenue, name='addvenue'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('', views.adminlogin, name='adminlogin'),
    path('logout/', views.logout_view, name='logout'),

  
]
