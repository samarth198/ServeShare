from django import forms
from .models import job_post,applicants


class job_post_form(forms.ModelForm):
    
    class Meta:
        model = job_post
        fields = ("title", "description", "venue", "compensation")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['venue'].widget.attrs.update({'class': 'form-control'})
        self.fields['compensation'].widget.attrs.update({'class': 'form-control'})


        
