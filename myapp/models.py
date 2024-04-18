from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    dob=models.DateField()
    profile_pic=models.ImageField(upload_to="profile",null=True,blank=True)
    options=(
        ("male","male"),("female","female")
    )
    gender=models.CharField(max_length=200,choices=options,default="male")
    address=models.CharField(max_length=200)
    phone=models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.user.username



class Video(models.Model):
    title=models.CharField(max_length=200)
    video_url = models.URLField(null=True)
    description=models.CharField(max_length=400)
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="video_profile")
    created_date=models.DateField(auto_now_add=True)


    def __str__(self) -> str:
        return self.title
