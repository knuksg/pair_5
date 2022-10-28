from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.http import require_POST
from accounts.forms import CustomUserCreationForm
from reviews.models import Review

# Create your views here.
def index(request):
    users = get_user_model().objects.all()


    context = {
        'users': users,
    }
    return render(request, 'accounts/index.html', context)

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('accounts:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

def detail(request, user_pk):
    user = get_user_model().objects.get(pk=user_pk)
    reviews = Review.objects.filter(user=user)
    
    followers = user.followers.all()
    followings = user.followings.all()
    
    context = {
        'user': user,
        'reviews': reviews,
        'followers': followers,
        'followings': followings,
    }
    return render(request, 'accounts/detail.html', context)

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'accounts:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)

def logout(request):
    auth_logout(request)
    
    return redirect('accounts:index')

@require_POST
def follow(request, user_pk):
    if request.user.is_authenticated:
        User = get_user_model()
        me = request.user
        you = User.objects.get(pk=user_pk) 
        if me != you:
            if you.followers.filter(pk=me.pk).exists(): 
                you.followers.remove(me)
                is_followed = False
            else: 
                you.followers.add(me) 
                is_followed = True
            context = {
            'is_followed': is_followed, 
            'followers_count': you.followers.count(), 
            'followings_count': you.followings.count(),
            }
            return JsonResponse(context)
        return redirect('accounts:detail', you.username)
    return redirect('accounts:login')
