"""
URL configuration for Heart project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Heart import views as view
from users import views as users
from admins import views as admins
from doctor import views as doctor


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view.index, name='index'),
    path('logout/', view.logout, name='logout'),



    path('UserLogin/', users.UserLogin, name='UserLogin'),
    path('UserRegisterAction/', users.UserRegisterAction, name='UserRegisterAction'),
    path('UserLoginCheck/', users.UserLoginCheck, name='UserLoginCheck'),
    path('UserAddData/', users.UserAddData, name='UserAddData'),
    path('UserDataView/', users.UserDataView, name='UserDataView'),
    path('UserMachineLearning/', users.UserMachineLearning, name='UserMachineLearning'),
    path('predictt/',users.predictt, name='predictt'),
    path('predictionss/', users.predictionss, name='predictionss'),


    path('AdminLogin/', admins.AdminLogin, name='AdminLogin'),
    path('AdminLoginCheck/', admins.AdminLoginCheck, name='AdminLoginCheck'),
    path('RegisterUsersView/', admins.RegisterUsersView, name='RegisterUsersView'),
    path('doctordetails/', admins.doctordetails, name='doctordetails'),
    path('activatedoctor/', admins.activatedoctor, name='activatedoctor'),
    path('ActivaUsers/', admins.ActivaUsers, name='ActivaUsers'),
    path('adminML/', admins.adminML, name='adminML'),

    path('doctorLogin/', doctor.doctorLogin, name='doctorLogin'),
    path('doctorregistrationaction/', doctor.doctorregistrationaction, name='doctorregistrationaction'),
    path('doctorlogincheck/', doctor.doctorlogincheck,name='doctorlogincheck'),
    path('doctorlogout/', doctor.doctorlogout, name='doctorlogout'),
    path('paitentdetails/', doctor.paitentdetails, name='paitentdetails'),
]
