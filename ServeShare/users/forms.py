from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from .models import OrganizationProfile,VolunteerProfile
from category.models import Category
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class VolunteerSignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    interests = forms.ModelMultipleChoiceField(required=False,
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-group'})
    )
    profile_picture = forms.ImageField(required=True, widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')   

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_volunteer = True
        if commit:
            user.save()
        volunteer = VolunteerProfile.objects.create(user=user, 
                                                   bio=self.cleaned_data.get('bio'),
                                                   first_name=self.cleaned_data.get('first_name'),
                                                   last_name=self.cleaned_data.get('last_name'),
                                                   profile_picture=self.cleaned_data.get('profile_picture'),
                                                   city=self.cleaned_data.get('city'),
                                                   state=self.cleaned_data.get('state'),
                                                   country=self.cleaned_data.get('country'))
        volunteer.interests.set(self.cleaned_data.get('interests'))
        return user


class OrganizationSignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    state = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    website = forms.URLField(widget=forms.URLInput(attrs={'class': 'form-control'}))
    established_year = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    causes_supported = forms.ModelMultipleChoiceField(required=False,
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-group'})
    )
    logo_picture = forms.ImageField(required=True, widget=forms.FileInput(attrs={'class': 'form-control-file'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')   

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_organization = True
        if commit:
            user.save()
        organization = OrganizationProfile.objects.create(user=user, 
                                                   phone_number=self.cleaned_data.get('phone_number'),
                                                   description=self.cleaned_data.get('description'),
                                                   address=self.cleaned_data.get('address'),
                                                   logo_picture=self.cleaned_data.get('logo_picture'),
                                                   website=self.cleaned_data.get('website'),
                                                   established_year=self.cleaned_data.get('established_year'),
                                                   name=self.cleaned_data.get('name'),
                                                   city=self.cleaned_data.get('city'),
                                                   state=self.cleaned_data.get('state'),
                                                   country=self.cleaned_data.get('country'))
        organization.causes_supported.set(self.cleaned_data.get('causes_supported'))
        return user