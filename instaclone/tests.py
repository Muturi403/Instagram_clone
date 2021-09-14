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
        
class ImageTestClass(TestCase):
	
    def setUp(self):
        self.new_user = User(username='Titus', email='titusouko@gmail.com', password='1234')
        self.new_user.save()
        self.new_profile = Profile(photo='image.png', bio='generous', user=self.new_user)
        self.new_profile.save()
        self.new_image = Image(name='Moringa', image='moringa.jpg', caption='wonderful place to be', profile=self.new_user, like_add=0)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_image,Image))

    def test_save_image(self):
        self.new_image.save_image()
        image = Image.objects.all()
        self.assertTrue(len(image)>0)

    def test_delete_image(self):
        self.new_image.save_image()
        self.new_image.delete_image()
        image = Image.objects.all()
        self.assertTrue(len(image)==0)       
        
class CommentsTest(TestCase):
	
    def setUp(self):
        self.new_user = User(username='Titus', email='titusouko@gmail.com', password='1234')
        self.new_user.save()
        self.new_image = Image(name='Moringa', image='moringa.jpg', caption='wonderful place to be', profile=self.new_user, like_add=0)
        self.new_image.save()
        self.new_comment = Comments(comment='This is a beautiful place',image=self.new_image,user=self.new_user)

    def test_instance(self):
        self.assertTrue(isinstance(self.new_comment, Comments))

    def test_save_comment(self):
        self.new_comment.save_comment()
        comment = Comments.objects.all()
        self.assertTrue(len(comment)>0)

    def test_delete_comment(self):
        self.new_comment.save_comment()
        self.new_comment.delete_comment()
        comment = Comments.objects.all()
        self.assertTrue(len(comment)==0)        