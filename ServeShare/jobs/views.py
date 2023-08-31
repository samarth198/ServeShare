from django.shortcuts import get_object_or_404, redirect, render
from .forms import job_post_form
from django.contrib.auth.decorators import login_required
from .models import job_post,applicants
from django.contrib.auth import get_user_model

User =  get_user_model()
# Create your views here.
@login_required(login_url='/users/login')
def post_job(request):
    if request.method == 'POST':
        form1 = job_post_form(request.POST)
        if form1.is_valid():
            job = form1.save(commit=False)
            job.posted_by= request.user
            job.save()
            return redirect('core:index')
    form1 = job_post_form
    return render(request,'jobs/post_job.html',({"job_form":form1}))

def jobs(request):
    jobs = job_post.objects.all().order_by('-created_at') 
    return render(request,'jobs/new_jobs.html',({"jobs":jobs}))

def job_desc(request,job_id):
    job = job_post.objects.get(pk = job_id)
    is_applicant = applicants.objects.filter(user=request.user, for_job=job).exists()
    if request.user.is_volunteer:
        if request.method == 'POST':
            ph = request.POST.get("phone")
            em = request.POST.get("email")
            u = request.user
            app = applicants.objects.create(user=u,for_job=job,email=em,phno=ph)
            app.save()
            return redirect('jobs:details',job_id=job_id)
    return render(request,'jobs/desc.html',({"job":job,"bool":is_applicant}))


def approve_applicant(request, job_id, user_id):
    job = get_object_or_404(job_post, pk=job_id)
    user = get_object_or_404(User, pk=user_id)
    
    job.approved.add(user.volunteer)
    job.save()
    
    return redirect('users:my_profile')

def disapprove_applicant(request, job_id, user_id):
    job = get_object_or_404(job_post, pk=job_id)
    user = get_object_or_404(User, pk=user_id)
    
    job.approved.remove(user.volunteer)
    job.save()
    
    return redirect('users:my_profile')