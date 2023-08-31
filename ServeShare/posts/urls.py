from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('post',views.normal_post,name='normal_post'),
    path('event-post',views.event_post,name='event_post'),
]
