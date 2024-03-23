"""
URL configuration for jobportal project.

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
from django.urls import path,include
from app1 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
    path('contact/', views.contact,name='contact'),
    path('', include('app1.urls')),
    path('emprsignup/',views.employersignup,name='emprsignup'),
    path('jobskrsignup/',views.jobseekersignup,name='jobskrsignup'),
    path('search/',views.search,name='search'),
    path('emprlogin/',views.employerlogin,name='emprlogin'),
    path('jobskrlogin/',views.jobseekerlogin,name='jobskrlogin'),
    path('emprhome/',views.employerhome,name='emprhome'),
    path('addjob/', include('app1.urls')),
    path('joblist/', include('app1.urls')),
    path('apcandidate/',views.appliedcandidate,name='apcandidate'),
    path('editjob/<int:pid>',views.editjob),
    path('editemprprofile/<int:pid>',views.editemprprofile),
    path('changeemprpassword/',views.changeemprpassword,name='changeemprpassword'),
    path('deletejob/<int:pid>',views.deletejob),
    path('latestjob/',views.latestjob),
    path('ujlist/',views.userjoblist),
    path('jobskrhome/',include('app1.urls')),
    path('editjobskrprofile/<int:pid>',views.editjobskrprofile),
    path('changejobskrpassword/',views.changejobskrpassword,name='changejobskrpassword'),
    path('ujdetail/<int:pid>',views.userjobdeail,name='userjobdetail'),
    path('applyjob/<int:pid>',views.applyjob,name='applyjob'),
    path('resume/',views.resume,name='resume'),
    path('logout/', views.Logout),
    path('acceptedcandidate/',views.acceptedcandidate,name='acceptedcandidate'),
    path('pendingcandidate/',views.pendingcandidate,name='pendingcandidate'),
    path('changestatus/',views.changestatus,name='changestatus'),
    path('reject_candidate/<int:candidate_id>',views.reject_candidate,name='reject_candidate'),
    path('jobskrjobstatus/', views.jobskrjobstatus, name='jobskrjobstatus'),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
