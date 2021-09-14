from django.db import models
import datetime as dt
from tinymce.models import HTMLField
from django.utils import timezone
from django.contrib.auth.models import User
import cloudinary
from cloudinary.models import CloudinaryField
from vote.models import VoteModel

# Create your models here.
class Profile(models.Model):
    '''
    User profile model
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    image = CloudinaryField('image', blank=True, null=True)
    biography = HTMLField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.biography

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def update_bio(cls,id, bio):
        update_profile = cls.objects.filter(id = id).update(bio = bio,)
        return update_profile

    @classmethod
    def get_all_profiles(cls):
        profile = Profile.objects.all()
        return profile
        
    @classmethod
    def search_user(cls,user):
        return cls.objects.filter(user__username__icontains=user).all()

