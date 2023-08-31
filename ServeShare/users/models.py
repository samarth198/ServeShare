from django.db import models
from django_resized import ResizedImageField
from django.contrib.auth.models import AbstractUser
from category.models import Category,Badge
from django.db.models.signals import post_save
from django.dispatch import receiver

class User(AbstractUser):
    is_volunteer = models.BooleanField(default=False)
    is_organization = models.BooleanField(default=False)
    email = models.EmailField()


class OrganizationProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='organization')
    
    name = models.CharField(max_length=50)
    logo_picture = ResizedImageField(size=[70,70] ,upload_to='organization_profile_pics/', blank=True, null=True)
    phone_number = models.CharField(max_length=100)
    description = models.TextField()
    city = models.CharField(max_length=50,null=True)
    state = models.CharField(max_length=50,null=True)
    country = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=150)
    website = models.URLField(blank=True)
    established_year = models.PositiveIntegerField(blank=True, null=True)
    joining_date = models.DateField(auto_now_add=True)
    causes_supported = models.ManyToManyField(Category, related_name='organizations',blank=True)
    verification_status = models.BooleanField(default=False)
    eco_points = models.PositiveIntegerField(default=0)
    following = models.ManyToManyField('self',related_name = 'followed_by_org',symmetrical=False)
    
    def __str__(self):
        return self.user.username 





class VolunteerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='volunteer')

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    bio = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    interests = models.ManyToManyField(Category, related_name='volunteers',blank=True)
    profile_picture = ResizedImageField(size=[70,70],upload_to='volunteer_profile_pics/', blank=True, null=True)
    joining_date = models.DateField(auto_now_add=True)
    eco_points = models.PositiveIntegerField(default=0)
    following = models.ManyToManyField(User,related_name='followed_by_volunteers',symmetrical=False)
    badges = models.ManyToManyField(Badge, related_name='awarded_volunteers',blank=True)
    rank = models.PositiveIntegerField(blank=True,null=True)


    
    def __str__(self):
        return self.user.username

    # badges = models.ManyToManyField(Badge, related_name='awarded_volunteers')

    def award_badges(self):
        for cat in Category.objects.all():
            events_participated = self.attended_events.filter(category=cat).count()
            badges_earned = Badge.objects.filter(category=cat, required_events__lte=events_participated)
            self.badges.add(*badges_earned)

    def calculate_rank(self):
        ranked_volunteers = VolunteerProfile.objects.order_by('-eco_points')
        d_rank = 1
        for volunteer in ranked_volunteers:
            if volunteer.eco_points == self.eco_points:
                self.rank = d_rank
                print(f"Found rank: {self.rank}")
                return
            d_rank += 1
        self.rank = d_rank 
        print(f"Found rank: {self.rank}")     
        self.save()
    
# @receiver(post_save, sender=VolunteerProfile)
# def assign_rank(sender, instance, **kwargs):
    


@receiver(post_save, sender=VolunteerProfile)
def update_badges(sender, instance, **kwargs):
    instance.calculate_rank()
    instance.award_badges()