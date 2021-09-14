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

class Image(VoteModel, models.Model):
    image_url = CloudinaryField('image', blank=True)
    imageName = models.CharField(max_length=100, blank=True)
    caption = models.CharField(max_length=500, blank=True)
    profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    like_add = models.PositiveIntegerField(default=0, blank=True)

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

    @classmethod
    def update_caption(self, caption):
        update_cap = cls.objects.filter(id = id).update(caption = caption)
        return update_cap
    
    @classmethod
    def get_all_images(cls):
        images = cls.objects.all()
        return images

    @classmethod
    def get_image_by_id(cls,id):
        image = cls.objects.filter(id= id).all()
        return image

    @classmethod
    def search_by_profile(cls,name):
        profile = Profile.objects.filter(user__name__icontains = name)

    @classmethod
    def get_one_image(cls,id):
        image = cls.objects.get(pk=id)
        return image

    def __str__(self):
        return self.imageName

    class Meta:
        ordering = ['-date_uploaded']


