from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class jobskrsignup(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mobile = models.IntegerField(max_length=15,null=True)
    gender = models.CharField(max_length=15,null=True)
    type = models.CharField(max_length=15,null=True)

    def __str__(self):
        return self.user.username
    
class emprsignup(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    company=models.CharField(max_length=100,null=True)
    mobile = models.IntegerField(max_length=15,null=True)
    type = models.CharField(max_length=15,null=True)
    
    def __str__(self):
        return self.user.username
    
class Job(models.Model):
    recruiter = models.ForeignKey(emprsignup,on_delete=models.CASCADE)
    startdate=models.DateField()
    enddate= models.DateField()
    title= models.CharField(max_length=100)
    salary= models.FloatField(max_length=20)
    description= models.CharField(max_length=300)
    experiance= models.CharField(max_length=50)
    location= models.CharField(max_length=100)
    skills= models.CharField(max_length=100)
    workmode = models.CharField(max_length=20,null=True)
    creationdate= models.DateField()
    
    def __str__(self):
        return self.title



class Apply(models.Model):
    job=models.ForeignKey(Job,on_delete=models.CASCADE)
    jsuser=models.ForeignKey(jobskrsignup,on_delete=models.CASCADE)
    resume=models.FileField(null=True)
    applydate=models.DateField()
    status = models.CharField(max_length=20, default='Pending') 
    
    
    def __str__(self):
        return f"{self.jsuser.user.username}"    

class Contact(models.Model):
    name=models.CharField(max_length=30)
    email=models.EmailField()
    phonenumber=models.IntegerField(max_length=15)
    description=models.TextField()
    
    
    def __str__(self):
        return self.email
    


# models.py

class Accept(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    jsuser = models.ForeignKey(jobskrsignup, on_delete=models.CASCADE)
    resume = models.FileField(null=True)
    acceptance_date = models.DateField()
    
    def __str__(self):
        return f"{self.jsuser.user.username} - {self.job.title}"
