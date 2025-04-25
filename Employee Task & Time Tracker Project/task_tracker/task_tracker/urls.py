"""
URL configuration for task_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
#from django.contrib import admin
#from django.urls import path

from django.urls import re_path
from time_tracker import views
from django.contrib import admin

urlpatterns = [

	re_path(r'^$', views.index, name='index'),
	re_path(r'^timesheet_success/(?P<in_or_out>\w+)/$', views.timesheet_success, name='timesheet_success'),
	re_path(r'^vacation_pending/$', views.vacation_pending, name='vacation_pending'),
	re_path(r'^mgnt_clocking/$', views.mgnt_clocking, name='mgnt_clocking'),
	re_path(r'^holiday_request/(?P<action>\w+)/(?P<holiday_request_id>\w+)/$', views.holiday_request_action, name='holiday_request_action'),
	re_path(r'^mgnt/$', views.login, name='login'),   		
	re_path(r'^auth_view/$', views.auth_view, name='auth_view'),  
	re_path(r'^logout/$', views.logout, name='logout'),
	re_path(r'^loggedin/$', views.loggedin, name='loggedin'),
	re_path(r'^invalid_login/$', views.invalid_login, name='invalid_login'),
               
]