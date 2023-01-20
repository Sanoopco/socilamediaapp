from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
# Create your models here.

class MyUser(AbstractUser):
    phone_no=models.CharField(max_length=50)
    profile_pic=models.ImageField(upload_to="profilepics",null=True,blank=True)
    # followers=models.ManyToManyField('Follow',blank=True)
    def __str__(self):
        return self.username

    @property
    def get_full_name(self):
        return super().get_full_name()
    @property
    def get_posts(self):
        posts= self.post_set.all()
        return posts

class Post(models.Model):
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    post_title=models.CharField(max_length=100)
    post_image=models.ImageField(upload_to='post-images',null=True,blank=True)
    post_desc=models.CharField(max_length=500)
    like=models.ManyToManyField(MyUser,related_name='like')
    created_date=models.DateTimeField(auto_now_add=True)

    @property
    def fetch_comments(self): 
        cmts=self.comments_set.all()
        return cmts

    def __str__(self):
        return self.post_title


    class Meta:
        ordering=('-created_date',)

class Comments(models.Model):
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    comment=models.CharField(max_length=200)
    created_date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment
    
    class Meta:
        ordering=('-created_date',)

class Saved(models.Model):
    user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
    saved_post=models.ForeignKey(Post,on_delete=models.CASCADE)
    def __str__(self):
        return self.post.post_title
    
# class Stories(models.Model):
#     user=models.ForeignKey(MyUser,on_delete=models.CASCADE)
#     story=models.FileField(upload_to='story-data')
#     created_date=models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering=('created_date',)

# class Follow(models.Model):
#     followed=models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name='user_followers')
#     followed_by=models.ForeignKey(MyUser,on_delete=models.CASCADE,related_name='user_follows')
#     def __str__(self):
#         return f"{self.followed_by.username} started following {self.followed.username}"
