from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model
from django_resized import ResizedImageField
from users.models import OrganizationProfile,VolunteerProfile
from category.models import Category
# Create your models here.

User = get_user_model()

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    datetime = models.DateTimeField()
    location = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="events_of")
    image = ResizedImageField(size=[480,380],upload_to='event_images/', blank=True, null=True)
    organizer = models.ForeignKey(OrganizationProfile, on_delete=models.CASCADE,related_name="events")
    duration = models.PositiveIntegerField()
    registered_volunteers = models.ManyToManyField(VolunteerProfile, related_name='events_registered', blank=True)
    attendees = models.ManyToManyField(VolunteerProfile, related_name='attended_events', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    has_finished = models.BooleanField(default=False)

    
    def __str__(self):
        return self.title

@receiver(pre_save, sender=Event)
def set_event_finished(sender, instance, **kwargs):
    if instance.datetime <= timezone.now():
        instance.has_finished = True
    else:
        instance.has_finished = False


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name="posts")
    title = models.CharField(max_length=100,blank=True)
    image = ResizedImageField(size=[480,380],upload_to='post_images/', blank=True, null=True)
    location = models.CharField(max_length=50,blank=True)
    caption = models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    org_tag = models.ForeignKey(OrganizationProfile,blank=True,null=True,on_delete=models.SET_NULL)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the parent class's save method
        if self.event and self.author.is_volunteer:
            volunteer = self.author.volunteer
            if volunteer not in self.event.attendees.all():
                self.event.attendees.add(volunteer)
                volunteer.eco_points += self.event.duration *10
                volunteer.save()

                ranked_volunteers = VolunteerProfile.objects.order_by('-eco_points')
                # d_rank = 1
                f = 0
                for a in ranked_volunteers:
                    if a.eco_points <= volunteer.eco_points:
                        volunteer.rank = a.rank
                        volunteer.save()
                        
                        if a.eco_points < volunteer.eco_points:
                            a.eco_points += 1

                        f = 1
                        break
                    d_rank += 1
                    if f==0:
                        volunteer.rank = d_rank 
                        volunteer.save()

                
            
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    Commenter = models.ForeignKey(User,on_delete=models.CASCADE)
    commented_at = models.DateField(auto_now_add=True)
    comment_text = models.TextField()