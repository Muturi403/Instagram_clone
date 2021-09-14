from django.test import TestCase
from .models import *
# Create your tests here.
class ProfileTest(TestCase):
	
    def setUp(self):
        self.new_user = User(username='Titus', email='titusouko@gmail.com', password='1234')
        self.new_user.save()
        self.new_profile = Profile(photo='image.png', bio='generous', user=self.new_user)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_profile, Profile))

    def test_save_method(self):
        self.new_profile.save_profile()
        profile = Profile.objects.all()
        self.assertTrue(len(profile)>0)
    
    def test_delete_method(self):
        self.new_profile.save_profile()
        self.new_profile.delete_profile()
        profile = Profile.objects.all()
        self.assertTrue(len(profile)==0)