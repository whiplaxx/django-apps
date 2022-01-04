from django.contrib.auth import forms
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm

class LoginView(auth_views.LoginView):
    template_name = 'users/login.html'
    next_page = reverse_lazy('users:profile')

def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))

def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'users/signup.html', {'form':form})
    elif request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('users:profile'))
        return render(request, 'users/signup.html', {'form':form})

@login_required(redirect_field_name=reverse_lazy('users:login'))
def profile(request):
    user = request.user
    return render(request, 'users/profile.html', {'user':user})

