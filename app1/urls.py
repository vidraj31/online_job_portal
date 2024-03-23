from django.urls import path
from app1 import views

urlpatterns = [
    path('signup/',views.signup),
    path('addjob/',views.addjob),
    path('jobskrhome/',views.jobseekerhome),
    path('joblist/',views.joblist,name='joblist'),
    
   
]