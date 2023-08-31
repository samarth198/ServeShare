from django.contrib import admin
from .models import OrganizationProfile,User,VolunteerProfile
# Register your models here.


admin.site.register(OrganizationProfile)
admin.site.register(VolunteerProfile)
admin.site.register(User)