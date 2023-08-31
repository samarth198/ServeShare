from django import forms
from .models import Event,Post

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'description', 'datetime', 'location', 'category', 'image', 'duration')
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'datetime': forms.DateTimeInput(attrs={'type':'datetime-local','class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'image', 'location', 'caption', 'org_tag', 'event')
        
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'caption': forms.Textarea(attrs={'class': 'form-control'}),
            'org_tag': forms.Select(attrs={'class': 'form-select'}),
            'event': forms.Select(attrs={'class': 'form-select'}),
        }
