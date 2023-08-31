from django.shortcuts import render,redirect
from django.utils import timezone
from posts.models import Post,Event
from users.models import VolunteerProfile,OrganizationProfile
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

User = get_user_model()

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        
        if request.user.is_volunteer :
            volunteer = VolunteerProfile.objects.get(user=request.user) 
            users_followed = volunteer.following.all()
            orgs_followed = OrganizationProfile.objects.filter(user__in=volunteer.following.all())
            post_list = Post.objects.all().filter(author__in = users_followed).order_by("-created_at")
            event_list = Event.objects.all().filter(organizer__in =  orgs_followed,has_finished = False).order_by("-created_at")
            if request.method == 'POST':
                if 'register' in request.POST:
                    event_id = request.POST.get('register')
                    event = Event.objects.get(pk = event_id)
                    if event.datetime > timezone.now():
                        event.registered_volunteers.add(request.user.volunteer)
                        event.save()
                        # send_mail('testing mail','here is message','serveshare.techtribe@gmail.com',[request.user.email],fail_silently=False)
                    return redirect('core:index')
                if 'unregister' in request.POST:
                    event_id = request.POST.get('unregister')
                    event = Event.objects.get(pk = event_id)
                    event.registered_volunteers.remove(request.user.volunteer)
                    event.save()
                    return redirect('core:index')
        else:
            organization = OrganizationProfile.objects.get(user=request.user)
            orgs_following = organization.following.all()
            user_following = User.objects.all().filter(organization__in = orgs_following)
            post_list = Post.objects.all().filter(author__in = user_following).order_by("-created_at")
            event_list = Event.objects.all().filter(organizer__in =  orgs_following,has_finished = False).order_by("-created_at")
        
        Post_list = Post.objects.exclude(id__in=post_list.values_list('id', flat=True)).order_by("-created_at")
        Event_list = Event.objects.exclude(id__in=event_list.values_list('id', flat=True)).order_by("-created_at")
        return render(request,'core/index.html',({"post_list":post_list,"event_list":event_list,"post_list_2":Post_list,"event_list_2":Event_list}))
    else:       
        post_list = Post.objects.all().order_by("-created_at")
        event_list = Event.objects.all().order_by("-created_at")
        
        return render(request,'core/index.html',({"post_list":post_list,"event_list":event_list}))

def leaderboard(request):
    rank_list = VolunteerProfile.objects.all().order_by('-eco_points')
    return render(request,'core/leaderboard.html',({"rank_list":rank_list}))