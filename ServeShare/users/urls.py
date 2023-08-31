from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path("register-volunteer",views.register_volunteer,name='register_volunteer'),
    path("register-organization",views.register_organization,name='register_organization'),
    path("login",views.login_user,name='login'),
    path("logout",views.logout_user,name='logout'),
    path("MyProfile",views.my_profile,name='my_profile'),
    path("<int:user_id>",views.profile_view,name='profile_view'),
]
