from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
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
    context = {
        'user': user,
        'reviews': reviews,
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

def follow(request, user_pk):
    user = get_user_model().objects.get(pk=user_pk)
    if request.user in user.followings.all():
        user.followings.remove(request.user)
    else:
        user.followings.add(request.user)
    return redirect('accounts:detail', user_pk)
