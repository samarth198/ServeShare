from django.contrib import admin
from .models import job_post,applicants
# Register your models here.
admin.site.register(job_post)
admin.site.register(applicants)