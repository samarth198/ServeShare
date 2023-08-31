from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    

class Badge(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='badge_images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    required_events = models.PositiveIntegerField()

    def __str__(self):
        return self.name
    
# class LeagueBadge(models.Model)