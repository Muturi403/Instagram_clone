from django.shortcuts import render, redirect
from django.http  import HttpResponse,Http404, HttpResponseRedirect
import datetime as dt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Image, Profile,Comments,Likes,Follow
from vote.managers import VotableManager
from .forms import ProfileForm, ImageForm, CommentForm
# Create your views here.

class SignupView(FormView):
    """Signup View."""
    template_name = 'registration/registration.html'
#     form_class = Signup
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """If the form is valid save the user"""
        form.save()
        return super().form_valid(form)


class LoginView(auth_views.LoginView):
    """Login view"""
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    """Logout View."""

class UpdateProfileView(LoginRequiredMixin, UpdateView):
    """Update a user's profile view"""
    template_name = 'update_profile.html'
    model = Profile
    fields = ['website', 'biography', 'phone_number', 'picture']
    def get_object(self):
        """Return user's profile"""
        return self.request.user.profile
    def get_success_url(self):
        """Return to user's profile."""
        username = self.object.user.username
        return reverse('users:detail', kwargs={'username_slug': username})


class UserDetailView(DetailView):
    """User detail view."""
    template_name = 'detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username_slug'
    queryset = User.objects.all()
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        """Add user's posts to context"""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['posts'] = Post.objects.filter(profile__user=user).order_by('-created')
        return context


votes=VotableManager()

def index(request):
    current_user = request.user
    posts = Image.get_all_images()
    comments = Comments.objects.all()
    profile = Profile.get_all_profiles()
    
    
    return render(request, 'all_files/index.html', locals())
    
@login_required(login_url='/registration/login/')
def add_image(request):
        current_user = request.user
        if request.method == 'POST':
                form = ImageForm(request.POST, request.FILES)
                if form.is_valid():
                        add=form.save(commit=False)
                        add.user = current_user
                        add.save()
                return redirect('home')
        else:
                form = ImageForm()
                return render(request,'image.html', {"form":form})

@login_required(login_url='/accounts/login/')                
def profile_info(request):
        current_user = request.user
        follow = Follow.objects.all().count()
        following = Follow.objects.all().count()
        # people_following = Follow.objects.following(request.user)
        profile = Profile.objects.filter(user=current_user).first()
        posts = request.user.image_set.all()
       
        return render(request, 'userProfile.html', {"images": posts, "profile": profile})

@login_required(login_url='/accounts/login/') 
def profile_update(request):
         current_user = request.user
         if request.method == 'POST':
                form = ProfileForm(request.POST, request.FILES)
                if form.is_valid():
                        add=form.save(commit=False)
                        add.user = current_user
                        add.save()
                return redirect('profile')
         else:
                form = ProfileForm()
         return render(request,'django_reg/profile_update.html',{"form":form})

@login_required(login_url='/accounts/login/') 
def comment(request,image_id):
        current_user=request.user
        image = Image.objects.get(id=image_id)
        profile_owner = User.objects.get(username=current_user.username)
        comments = Comments.objects.all()
        
        if request.method == 'POST':
                form = CommentForm(request.POST, request.FILES)
                if form.is_valid():
                        comment = form.save(commit=False)
                        comment.image = image
                        comment.user = request.user
                        comment.save()
            
                       
                return redirect('home')
        else:
                form = CommentForm()
        return render(request, 'comment.html',locals())   

@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'username' in request.GET and request.GET["username"]:
        search_term = request.GET.get("username")
        searched_users = User.objects.filter(username__icontains = search_term)
        message = f"{search_term}"
        profile_pic = User.objects.all()
        return render(request, 'all_files/search.html', {'message':message, 'results':searched_users, 'profile_pic':profile_pic})
    else:
        message = "You haven't searched for any term"
        return render(request, 'all_files/search.html', {'message':message})

def search(request):
    profiles = User.objects.all()
    if 'username' in request.GET and request.GET['username']:
        search_term = request.GET.get('username')
        results = User.objects.filter(username__icontains=search_term)
        return render(request,'search.html',locals())
    return redirect(home)  

def follow(request, user_id):
    other_user = User.objects.get(id = user_id)
    follow = Follow.objects.add_follower(request.user, other_user)

    return redirect('home')

def unfollow(request, user_id):
    other_user = User.objects.get(id = user_id)
    follow = Follow.objects.remove_follower(request.user, other_user)

    return redirect('home')



@login_required(login_url='/accounts/register/')
def like_images(request, id):
        image = Image.get_one_image(id)
        user = request.user
        user_id = user.id

        if user.is_authenticated:
                uplike = image.votes.up(user_id)
                image.like_add = image.votes.count()
                image.save()

        return redirect('home')