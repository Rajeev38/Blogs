from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import F
import datetime


def index(request):
    if request.method == 'POST':
        error = ''
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            request.session['username'] = request.POST['username']
            return redirect('blogs')
    else:
        if 'username' in request.session:
            return redirect('blogs')
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
    if request.method == 'POST':
        author = User.objects.filter(username=request.session['username'])
        name = request.POST['name']
        content = request.POST['content']
        blog = Blog(name=name, content=content, author=author[0])
        blog.save()
        return redirect('blogs')


@login_required(login_url='')
def showblogs(request):
    blog = Blog.objects.all().order_by('-modified_at')
    return render(request, 'blogs.html', {'allblogs': blog})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required(login_url='')
def myblogs(request):
    allblogs = Blog.objects.filter(author__username=request.session['username']).order_by('-modified_at')
    return render(request, 'myblogs.html', {'allblogs': allblogs})


@login_required(login_url='')
def detail_view(request, id=None):
    blog = Blog.objects.filter(id=id)
    comments = Comment.objects.filter(blog=blog[0]).order_by('-created_date')
    count = Comment.objects.filter(blog=blog[0]).count()
    response1 = Response.objects.filter(blog=blog[0], like_or_not=True).count()
    response2 = Response.objects.filter(blog=blog[0], like_or_not=False).count()
    response3 = Response.objects.filter(blog=blog[0], user__username=request.session['username'])
    flag = None
    if response3:
        flag = response3[0].like_or_not
        if flag == True:
            flag = 'Liked'
        else:
            flag = 'Disliked'
    params = {'blog': blog[0], 'comments': comments, 'count': count, 'response1': response1,
              'response2': response2, 'flag': flag}
    return render(request, 'details.html', params)


@login_required(login_url='')
def addcomment(request, id=None):
    if request.method == 'POST':
        blog = Blog.objects.filter(id=id)
        user = User.objects.filter(username=request.session['username'])
        text = request.POST['content']
        # blog = Blog.obejects.filter(id=request.POST['id'])
        comment = Comment(blog=blog[0], user=user[0], comment_text=text)
        comment.save()
        return redirect('details', id)

    else:
        return redirect('details', id)


@login_required(login_url='')
def like_view(request, id=None):
    date1 = datetime.datetime.today()
    blog = Blog.objects.filter(id=id)
    user = User.objects.filter(username=request.session['username'])
    response = Response.objects.update_or_create(blog=blog[0], user=user[0], defaults={'like_or_not': True,'response_date':date1})
    return redirect('details', id)


@login_required(login_url='')
def dislike_view(request, id=None):
    date1 = datetime.datetime.today()
    blog = Blog.objects.filter(id=id)
    user = User.objects.filter(username=request.session['username'])
    response = Response.objects.update_or_create(blog=blog[0], user=user[0], defaults={'like_or_not': False,'response_date':date1})
    return redirect('details', id)


@login_required(login_url='')
def modify_view(request, id=None):
    params = {'id': id}
    return render(request, 'modify.html', params)


@login_required(login_url='')
def modified(request):
    if request.method == 'POST':
        id = request.POST['id']
        name = request.POST['name']
        content = request.POST['content']
        blog = Blog.objects.update_or_create(id=id, author__username=request.session['username'],
                                             defaults={'name': name, 'content': content, 'is_modified': True})
        return redirect('myblogs')


@login_required(login_url='')
def quick_view(request):
    date1 = datetime.datetime.today()
    date2 = date1 - datetime.timedelta(days=3)
    comments = Blog.objects.filter(comment__user__username=request.session['username']
                                   ).order_by('-created_at').distinct()[:5]

    params = {'comments': comments}

    return render(request, 'quick_view.html', params)


@login_required(login_url='')
def historybyblog_view(request, id=None):
    blog = Blog.objects.filter(id=id)
    user = User.objects.filter(username=request.session['username'])
    comments = Comment.objects.filter(blog=blog[0], user=user[0])
    params = {'blog': blog[0], 'comments': comments}
    return render(request, 'historybyblog.html', params)


@login_required(login_url='')
def historybyauth_view(request, data=None):
    blog = Blog.objects.filter(author__username=data, comment__user__username=request.session['username'])
    return render(request, 'historybyauthor.html', {'blog': blog})


def liked(request):
    date1 = datetime.datetime.today()
    date2 = date1 - datetime.timedelta(days=3)
    print(date1)
    print(date2)
    liked = Blog.objects.filter(response__user__username=request.session['username'],
                                response__response_date__gt=date2, response__like_or_not=True).order_by('-created_at')[:5]
    #print(liked[0])
    params = {'liked': liked}
    return render(request, 'liked.html', params)


def disliked(request):
    date1 = datetime.datetime.today()
    date2 = date1 - datetime.timedelta(days=3)
    disliked = Blog.objects.filter(response__user__username=request.session['username'],
                                   response__response_date__gt=date2, response__like_or_not=False).order_by('-created_at')[:5]
    params = {'disliked': disliked}
    return render(request, 'disliked.html', params)


def unmodified(request):
    unmodified = Blog.objects.filter(author__username=request.session['username'],
                                     is_modified=False)
    params = {'unmodified': unmodified}
    return render(request, 'unmodified.html', params)


def allcomments(request):
    commented = Blog.objects.filter(comment__user__username=request.session['username']).distinct()
    params = {'commented': commented}
    return render(request, 'allcomments.html', params)
