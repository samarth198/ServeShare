from django.shortcuts import render,redirect
from .forms import PostForm,EventForm
from django.contrib.auth.decorators import login_required
from users.decorators import organization_required,volunteer_required
# from djjango


# Create your views here.
@login_required(login_url='/users/login')
def normal_post(request):
        if request.method == 'POST':
            if 'add_post' in request.POST:
                form1 = PostForm(request.POST,request.FILES)
                if form1.is_valid():
                    post = form1.save(commit=False)
                    post.author = request.user
                    post.save()
                    return redirect('core:index')
        form1 = PostForm
        return render(request,'posts/post1.html',({"post_form":form1}))


@login_required(login_url='/users/login')
@organization_required
def event_post(request):                   
        if request.method == 'POST':
            if 'add_event' in request.POST:
                form2 = EventForm(request.POST,request.FILES or None)
                if form2.is_valid():
                    event = form2.save(commit=False)
                    event.organizer = request.user.organization
                    event.save()
                    return redirect('core:index')
        form2 = EventForm
        return render(request,'posts/event.html',({"event_form":form2}))
