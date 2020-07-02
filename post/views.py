from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .myforms import SignupForm
from .models import *
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    if request.method == 'POST':
        error = ''
        form = AuthenticationForm(data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            request.session['username'] = request.POST['username']
            return redirect('blogs')
    else:
        form = AuthenticationForm()
    return render(request, 'index.html', {'form': form})


def signUp(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm
    return render(request, 'signup.html', {'form': form})


@login_required(login_url='')
def createblog(request):
    print(request.session['username'])
    if request.method == 'POST':
        author = User.objects.filter(username=request.session['username'])
        name = request.POST['name']
        content = request.POST['content']
        blog = Blog(name=name, content=content, author=author[0])
        blog.save()
        return redirect('blogs')


@login_required(login_url='')
def showblogs(request):
    blog = Blog.objects.all()
    return render(request, 'blogs.html', {'allblogs': blog})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required(login_url='')
def myblogs(request):
    allblogs = Blog.objects.filter(author__username=request.session['username'])
    return render(request, 'myblogs.html', {'allblogs': allblogs})
