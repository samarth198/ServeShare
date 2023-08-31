from django.db import models
from django.contrib.auth import get_user_model
from users.models import VolunteerProfile

User = get_user_model()
# Create your models here.
class job_post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    venue = models.CharField(max_length=200)
    compensation = models.DecimalField(max_digits=10, decimal_places=2)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='jobs_by')
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.ManyToManyField(VolunteerProfile,related_name="my_jobs")

    def __str__(self):
        return self.title
    
class applicants(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="my_applications")
    for_job =models.ForeignKey(job_post,on_delete=models.CASCADE,related_name="applicants")
    email = models.EmailField()
    phno = models.CharField(max_length=10) 