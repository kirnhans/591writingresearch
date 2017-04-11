from django import forms

from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from models import *

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(max_length = 200, 
                                label='Password', 
                                widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 200, 
                                label='Confirm password',  
                                widget = forms.PasswordInput())
    username = forms.CharField(max_length = 200)
    email = forms.CharField(max_length = 200)
    class Meta:
        model = Profile
        fields = ['username','first_name','last_name','email','password1','password2']
        # exclude = ['picture','location','birthday','following', 'bio', 'user','password'] #need to have two password fields

        #customize for passwords
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        
         # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).count() > 0:
            raise forms.ValidationError("A student with username %s already exists." % username)
        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
        return username


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['text']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text','post']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'following']
        widgets = {'picture': forms.FileInput()}

class PasswordForm(forms.ModelForm):
    old_password = forms.CharField(max_length = 200, 
                                widget = forms.PasswordInput())
    password1 = forms.CharField(max_length = 200, 
                                label='New password', 
                                widget = forms.PasswordInput())
    password2 = forms.CharField(max_length = 200, 
                                label='Confirm new password',  
                                widget = forms.PasswordInput())

    def __init__(self,request=None,user=None):
        if (request==None or user==None):
            super(PasswordForm,self).__init__()
        else:
            self.user=user
            super(PasswordForm,self).__init__(request)

    #have to do this to access the profile
    class Meta:
        model = Profile
        fields = []


    def clean(self):
        cleaned_data = super(PasswordForm, self).clean()
        
         # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data

    def clean_old_password(self):
        username = self.user.username
        old_password = self.cleaned_data.get('old_password')
        user = authenticate(username=username,password=old_password)
        if user==None:
            raise forms.ValidationError("Password does not match old password.")
        return old_password