from django import forms
from igramapp.models import MyUser,Post
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm

class RegistrationForm(UserCreationForm):
    password1=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))
    class Meta:
        model=MyUser
        fields=[
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_no",
            "profile_pic",
            "password1",
            "password2"
            ]
        widgets={
            "first_name":forms.TextInput(attrs={"class":"form-control"}),
            "last_name":forms.TextInput(attrs={"class":"form-control"}),
            "username":forms.TextInput(attrs={"class":"form-control"}),
            "email":forms.EmailInput(attrs={"class":"form-control"}),
            "phone_no":forms.TextInput(attrs={"class":"form-control"}),
            "profile_pic":forms.FileInput(attrs={"class":"form-control-file"})
        }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=[
            'post_title',
            'post_image',
            'post_desc'
        ]
        widgets={
            'post_title':forms.TextInput(attrs={'class':'form-control'}),
            'post_image':forms.FileInput(attrs={'class':'form-control'}),
            'post_desc':forms.Textarea(attrs={'class':'form-control','rows':5}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=MyUser
        fields=[
            'username',
            'first_name',
            'last_name',
            'profile_pic'
            ]
        widgets={
            'username':forms.TextInput(attrs={"class":'form-control'}),
            'first_name':forms.TextInput(attrs={"class":'form-control'}),
            'last_name':forms.TextInput(attrs={"class":'form-control'}),
            'profile_pic':forms.FileInput(attrs={"class":'form-control'}),
        }

class ChangePasswordForm(PasswordChangeForm):
    old_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control mt-2'}))
    new_password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control mt-2'}))
    new_password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control mt-2'}))
    