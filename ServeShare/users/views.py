from django.shortcuts import render,redirect
from .forms import OrganizationSignUpForm,VolunteerSignUpForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from category.models import Category,Badge
# from jobs.models import job_post

User = get_user_model()
# Create your views here.

def register_organization(request):
    if request.method == "POST":
        form = OrganizationSignUpForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            request.user.organization.following.add(request.user.organization)
            return redirect('core:index')
    else:
        form = OrganizationSignUpForm()
    return render(request,'users/register_organisation.html',({'form':form}))

def register_volunteer(request):
    if request.method == "POST":
        form = VolunteerSignUpForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            request.user.volunteer.following.add(request.user)
            return redirect('core:index')
    else:
        form = VolunteerSignUpForm()
    return render(request,'users/register_volunteer.html',({'form':form}))

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect("core:index")
        else:
            messages.success(request,("Enter correct username and password"))
            return redirect("users:login")
    else:
        
        return render(request,"users/login_user.html")   
    
@login_required(login_url='users/login')
def logout_user(request):
    logout(request)
    return redirect('core:index')

@login_required(login_url='/users/login')
def my_profile(request):
    jobs = request.user.jobs_by.all()
    if request.user.is_volunteer:
        followers_count = request.user.followed_by_volunteers.all().count()
        follow_count = request.user.volunteer.following.all().count()

        badges = Badge.objects.all()
        badge_data = []
        for badge in badges:
            events_participated = request.user.volunteer.attended_events.filter(category=badge.category).count()
            total_events = badge.required_events
            image = badge.image
            progress_percentage = (events_participated / total_events) * 100 if total_events > 0 else 0
            badge_data.append({
                'name': badge.name,
                'events_participated': events_participated,
                'total_events': total_events,
                'progress_percentage': progress_percentage,
                "image":image,
            })

        context = {
            "followers": followers_count,
            "following": follow_count,
            "jobs":jobs,
            "badges": badge_data,  # Pass the badge data list to the context
        }
        return render(request, 'users/profile.html', context)

    if request.user.is_organization:
        followers_count = request.user.organization.followed_by_org.all().count()
        follow_count = request.user.organization.following.all().count()
        return render(request,'users/org_profile.html',({"followers":followers_count,"following":follow_count,"jobs":jobs}))
    

def profile_view(request,user_id):
    u = User.objects.get(pk = user_id)
    if request.user == u:
        jobs = request.user.jobs_by.all()
        if request.user.is_volunteer:
            followers_count = request.user.followed_by_volunteers.all().count()
            follow_count = request.user.volunteer.following.all().count()

            badges = Badge.objects.all()
            badge_data = []
            for badge in badges:
                events_participated = request.user.volunteer.attended_events.filter(category=badge.category).count()
                total_events = badge.required_events
                image = badge.image
                progress_percentage = (events_participated / total_events) * 100 if total_events > 0 else 0
                badge_data.append({
                    'name': badge.name,
                    'events_participated': events_participated,
                    'total_events': total_events,
                    'progress_percentage': progress_percentage,
                    "image":image,
                })

            context = {
                "followers": followers_count,
                "following": follow_count,
                "jobs":jobs,
                "badges": badge_data,  # Pass the badge data list to the context
            }
            return render(request, 'users/profile.html', context)

        if request.user.is_organization:
            followers_count = request.user.organization.followed_by_org.all().count()
            follow_count = request.user.organization.following.all().count()
            return render(request,'users/org_profile.html',({"followers":followers_count,"following":follow_count,"jobs":jobs}))

    if u.is_volunteer:
        followers_count = u.followed_by_volunteers.all().count()
        follow_count = u.volunteer.following.all().count()
        if request.method == "POST":
            if 'follow' in request.POST:
                key = request.POST.get('follow')
                utf = User.objects.get(pk=key)
                request.user.volunteer.following.add(utf)
                request.user.save()
            if 'unfollow' in request.POST:
                key = request.POST.get('unfollow')
                utf = User.objects.get(pk=key)
                request.user.volunteer.following.remove(utf)
                request.user.save()
        return render(request,'users/vol_profile.html',({'u':u,"followers":followers_count,"following":follow_count}))
    if u.is_organization:
        followers_count = u.organization.followed_by_org.all().count()
        follow_count = u.organization.following.all().count()
        if request.method == "POST":
            if request.user.is_volunteer:
                if 'follow' in request.POST:
                    key = request.POST.get('follow')
                    utf = User.objects.get(pk=key)
                    request.user.volunteer.following.add(utf)
                    request.user.save()
                if 'unfollow' in request.POST:
                    key = request.POST.get('unfollow')
                    utf = User.objects.get(pk=key)
                    request.user.volunteer.following.remove(utf)
                    request.user.volunteer.save()
            if request.user.is_organization:
                if 'followo' in request.POST:
                    key = request.POST.get('followo')
                    utf = User.objects.get(pk=key)
                    request.user.organization.following.add(utf.organization)
                    request.user.save()
                if 'unfollowo' in request.POST:
                    key = request.POST.get('unfollowo')
                    utf = User.objects.get(pk=key)
                    request.user.organization.following.remove(utf.organization)
                    request.user.organization.save()
        return render(request,'users/organ_profile.html',({'u':u,"followers":followers_count,"following":follow_count}))