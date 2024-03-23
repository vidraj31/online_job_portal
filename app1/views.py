from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from datetime import date
from django.contrib import messages



# Create your views here.
def home(request):
    job=Job.objects.all().order_by('-startdate')
    d={'job':job}
    return render(request,'home.html',d)

def search(request):
    query=request.GET['search']
    if len(query)>100:
        job=Job.objects.none()
    else:
        jobTitle=Job.objects.filter(title__icontains=query) 
        jobDescription=Job.objects.filter(description__icontains=query)
        job=jobTitle.union(jobDescription)
    if job.count()==0:
        messages.warning(request,"No Search Result")  
    d={'job':job,'query':query}           
    return render(request,'search.html',d)

def contact(request):
    if request.method=="POST":
        fname=request.POST.get("name")
        femail=request.POST.get("email")
        phone=request.POST.get("phone")
        desc=request.POST.get("desc")
        query=Contact(name=fname,email=femail,phonenumber=phone,description=desc)
        query.save()

       

        messages.info(request,"Thanks For reaching Us! We will get back you soon....")
        return redirect('contact')
    return render(request,'contact.html')


def signup(request):
    return render(request,'signup/signup.html')

def employersignup(request):
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        p = request.POST['pass1']
        cp= request.POST['pass2']
        e = request.POST['email']
        m = request.POST['mobile']
        c = request.POST['cname']

        if p != cp:
            messages.warning(request,"Password is Incorrect")
            return redirect('/emprsignup')
        
        try:
            if User.objects.get(username=e):
                messages.info(request,"Email is already exist")
                return redirect('/emprsignup')
        except:
            pass  

        try:
            if emprsignup.objects.get(mobile=m):
                messages.info(request,"Mobilenumber is already exist")
                return redirect('/emprsignup')
        except:
            pass   
        
        
        user=User.objects.create_user(first_name=f,last_name=l,username=e,password=p)
        emprsignup.objects.create(user=user,company=c,mobile=m,type="employer")
        return redirect('/emprlogin')
    return render(request,'signup/emprsignup.html')

def employerlogin(request):
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pass1']
        user = authenticate(username=u, password=p)

        if user is not None:
            try:
                user1 = emprsignup.objects.get(user=user)
                if user1.type == "employer":
                    login(request, user)
                    return redirect('/emprhome')
                else:
                    messages.error(request, "Invalid Credentials")
            except emprsignup.DoesNotExist:
                messages.error(request, "User does not exist.")
        else:
            messages.error(request, "Invalid Credentials")

    return render(request,'login/emprlogin.html')

def jobseekersignup(request):
     if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        p = request.POST['pass1']
        cp= request.POST['pass2']
        e = request.POST['email']
        m = request.POST['mobile']
        g = request.POST['gender']
        if p != cp:
            messages.warning(request,"Password is Incorrect")
            return redirect('/jobskrsignup')
        
        try:
            if User.objects.get(username=e):
                messages.info(request,"Email is already exist")
                return redirect('/jobskrsignup')
        except:
            pass  

        try:
            if jobskrsignup.objects.get(mobile=m):
                messages.info(request,"Mobilenumber is already exist")
                return redirect('/jobskrsignup')
        except:
            pass   
        
        
        user=User.objects.create_user(first_name=f,last_name=l,username=e,password=p)
        jobskrsignup.objects.create(user=user,mobile=m,gender=g,type="jobseeker")
        return redirect('/jobskrlogin')
        
     return render(request,'signup/jobskrsignup.html')

def jobseekerlogin(request):
    if request.method=='POST':
        u = request.POST['uname'] 
        p = request.POST['pass1']
        user = authenticate(username=u,password=p)
        if user is not None:
            try:
                user1 = jobskrsignup.objects.get(user=user)
                if user1.type == "jobseeker":
                    login(request, user)
                    return redirect('/jobskrhome')
                else:
                    messages.error(request, "Invalid Credentials")
            except jobskrsignup.DoesNotExist:
                messages.error(request, "User does not exist.")
        else:
            messages.error(request, "Invalid Credentials")
    return render(request,'login/jobskrlogin.html')


def employerhome(request):
    if not request.user.is_authenticated:
        return redirect('emprlogin')
    job = emprsignup.objects.get(user=request.user)
    d={'job':job}
    return render(request,'empr/emprhome.html',d)     

def addjob(request):
    if not request.user.is_authenticated:
        return redirect('emprlogin')
    error=""
    if request.method=='POST':
        j = request.POST['jobtitle']
        s = request.POST['startdate']
        e = request.POST['enddate']
        sa = request.POST['salary']
        l = request.POST['location']
        ex = request.POST['experiance']
        sk = request.POST['skills']
        de = request.POST['description']
        wm = request.POST['workmode']
        user=request.user
        recruiter=emprsignup.objects.get(user=user)
        try:
            Job.objects.create(recruiter=recruiter,startdate=s,enddate=e,title=j,salary=sa,description=de,experiance=ex,workmode=wm, location=l,skills=sk,creationdate=date.today())
            error="no"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'empr/addjob.html',d)

def joblist(request):
    if not request.user.is_authenticated:
        return redirect('emprlogin')
    user=request.user
    recruiter=emprsignup.objects.get(user=user)
    job=Job.objects.filter(recruiter=recruiter)
    d={'job':job}
    return render(request,'empr/joblist.html',d)

def editjob(request,pid):
     if not request.user.is_authenticated:
        return redirect('emprlogin')
     error=""
     job=Job.objects.get(id=pid)
     if request.method=='POST':
        j = request.POST['jobtitle']
        s = request.POST['startdate']
        e = request.POST['enddate']
        sa = request.POST['salary']
        l = request.POST['location']
        ex = request.POST['experiance']
        sk = request.POST['skills']
        de = request.POST['description']
        wm = request.POST['workmode']
        
        job.title=j
        job.salary=sa
        job.location=l
        job.experiance=ex
        job.skills=sk
        job.description=de
        job.workmode=wm
        try:
            job.save()
            error="no"
        except:
            error="yes"
        if s:
            try:
                job.startdate=s
                job.save()
            except:
                pass

        else:
            pass
        if e:
            try:
                job.enddate=e
                job.save()
            except:
                pass

        else:
            pass
     d = {'error':error,'job':job}
     return render(request,'empr/editjob.html',d)

def editemprprofile(request,pid):
     if not request.user.is_authenticated:
        return redirect('emprlogin')
     error=""
     job=emprsignup.objects.get(id=pid)
     if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        m = request.POST['mobile']
        c = request.POST['cname']
        
        job.user.first_name=f
        job.user.last_name=l
        job.user.username=e
        job.mobile=m
        job.company=c
        try:
            job.save()
            job.user.save()
            error="no"
        except:
            error="yes"
        
     d = {'error':error,'job':job}
     return render(request,'empr/editemprprofile.html',d)

def changeemprpassword(request):
     if not request.user.is_authenticated:
        return redirect('emprlogin')
     error=""
     if request.method=='POST':
         c=request.POST['currentpassword']
         n=request.POST['newpassword']
         try:
             u=User.objects.get(id=request.user.id)
             if u.check_password(c):
                 u.set_password(n)
                 u.save()
                 error='no'
             else:
                 error='no'
         except: 
             error='yes'   
     d={'error':error}        
     return render(request,'empr/changeemprpassword.html',d)

def deletejob(request,pid):
     if not request.user.is_authenticated:
        return redirect('emprlogin')
     job=Job.objects.get(id=pid)
     job.delete()
     return redirect('joblist')


def appliedcandidate(request):
    if not request.user.is_authenticated:
        return redirect('emprlogin')
    
    data=Apply.objects.all()

    d={'data':data}
    return render(request,'empr/appliedcandidate.html',d)

def jobseekerhome(request):
    if not request.user.is_authenticated:
        return redirect('jobskrlogin')
    
    job = jobskrsignup.objects.get(user=request.user)
    d={'job':job}

    return render(request,'jk/jobskrhome.html',d)


def editjobskrprofile(request,pid):
     if not request.user.is_authenticated:
        return redirect('jobskrlogin')
     error=""
     job=jobskrsignup.objects.get(id=pid)
     if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        m = request.POST['mobile']
        g = request.POST['gender']
        
        job.user.first_name=f
        job.user.last_name=l
        job.user.username=e
        job.mobile=m
        job.gender=g
        try:
            job.save()
            job.user.save()
            error="no"
        except:
            error="yes"
        
     d = {'error':error,'job':job}
     return render(request,'jk/editjobskrprofile.html',d)

def changejobskrpassword(request):
     if not request.user.is_authenticated:
        return redirect('jobskrlogin')
     error=""
     if request.method=='POST':
         c=request.POST['currentpassword']
         n=request.POST['newpassword']
         try:
             u=User.objects.get(id=request.user.id)
             if u.check_password(c):
                 u.set_password(n)
                 u.save()
                 error='no'
             else:
                 error='no'
         except: 
             error='yes'   
     d={'error':error}        
     return render(request,'jk/changejobskrpassword.html',d)



def userjoblist(request):
    job=Job.objects.all().order_by('-startdate')
    user=request.user
    jsuser=jobskrsignup.objects.get(user=user)
    data=Apply.objects.filter(jsuser=jsuser)
    li=[]
    for i in data:
        li.append(i.job.id)
    d={'job':job,'li':li}
    return render(request,'jk/userjoblist.html',d)


def latestjob(request):
    job=Job.objects.all().order_by('-startdate')
    d={'job':job}
    return render(request,'latestjob.html',d)

def userjobdeail(request,pid):
    job=Job.objects.get(id=pid)
    d={'job':job}
    return render(request,'jk/userjobdetail.html',d)


def applyjob(request,pid):
    if not request.user.is_authenticated:
     return redirect('jobskrlogin')
    data =jobskrsignup.objects.get(user=request.user)
    error=""
    user=request.user
    jsuser=jobskrsignup.objects.get(user=user)
    job=Job.objects.get(id=pid)
    date1=date.today()
    if job.enddate<date1:
     error="close"
    elif job.startdate>date1:
      error="notopen"
    else:
        if request.method=='POST':
            r=request.FILES['resume']
            Apply.objects.create(job=job,jsuser=jsuser,resume=r,applydate=date.today())
            error="done"
    d={'error':error,'data':data}  
    return render(request,'jk/applyjob.html',d)

def resume(request):
    return render(request,'jk/resume.html')

def Logout(request):
    logout(request)
    return redirect('home')

def acceptedcandidate(request):
    if not request.user.is_authenticated:
        return redirect('emprlogin')

    # Get the accepted candidates for the current employer
    accepted_candidates = Accept.objects.filter(job__recruiter__user=request.user)

    # Pass the data to the template
    context = {'data': accepted_candidates}
    return render(request, 'empr/acceptedcandidate.html', context)   



def pendingcandidate(request):
    if not request.user.is_authenticated:
        return redirect('emprlogin')
    data=Apply.objects.filter(status='Pending')
    d={'data':data}
    return render(request,'empr/pendingcandidate.html',d)


def changestatus(request,pid):
    if not request.user.is_authenticated:
        return redirect('emprlogin')
    data=Apply.objects.get(id=pid)
    d={'data':data}
    return render(request,'empr/pendingcandidate.html',d)




def reject_candidate(request, candidate_id):
    candidate = Job.objects.get(id=candidate_id)
    # Perform any logic you need for rejecting the candidate, e.g., updating status
    candidate.status = 'Rejected'
    candidate.save()
    messages.success(request, 'Candidate rejected successfully.')
    return redirect('apcandidate')


def jobskrjobstatus(request):
    if not request.user.is_authenticated:
        return redirect('jobskrlogin')

    # Get the applied jobs for the current user
    applied_jobs = Apply.objects.filter(jsuser__user=request.user)

    # Pass the data to the template
    context = {'data': applied_jobs}
    return render(request, 'jk/jobstatus.html', context)
