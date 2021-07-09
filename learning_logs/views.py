from django.shortcuts import redirect, render

from django.http import HttpResponse, HttpResponseRedirect, request
from django.db.models import Count
from .models import topic, entry, Comment, likes, Category, Subscriber
from .forms import MyForm, LoginForm, EditForm
from django.views.decorators.csrf import csrf_exempt
from .models import topic, entry
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import os

import random
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def random_digits():
    return "%0.12d" % random.randint(0, 999999999999)

# Home page / Base template


def index(request):
    entries_ = entry.objects.all().order_by('date_added')
    top_rated = entry.objects.annotate(
        no_of_likes=Count('likes')).order_by('-no_of_likes')[:2]

    return render(request, 'learning_logs/base.html', {'entries': entries_,   'top_rated': top_rated})


# Topics views
def topics(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            topics = topic.objects.filter(
                user__id=request.user.id).annotate(dcount=Count('article_name')).order_by('date_added')

            # entry_set = entry.objects.filter(user__id = request.user)

            context = {'topics': topics}
            return render(request, 'learning_logs/topics.html', context)
    else:
        return redirect('/login')


# Getting entry by topic name

def topic_a(request, art_name):
    # show single topics
    if request.method == "GET":
        cat_ins = Category.objects.get(name=art_name)
        topics = topic.objects.filter(article_name=cat_ins)
        context = {'topics': topics,
                   'disp': True
                   }
        return render(request, 'learning_logs/categories.html', context)


# Blog Views
@csrf_exempt
def give_data(request):
    if request.method == 'POST':
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        uname = request.POST['username']
        email_add = request.POST['email']
        password = request.POST['password']
        new_user = User.objects.create_user(first_name=fname, last_name=lname,
                                            username=uname, email=email_add, password=password)

        new_user.save()
        # sub=Subscriber.objects.create(email=email_add,conf_num=random_digits())
        # new_user.save()
        # sub.save()

        return HttpResponseRedirect('/login')

    return render(request, 'learning_logs/data_form.html')

# login form


@csrf_exempt
def login_form(request):
    # login form
    if request.method == 'POST':
        check = request.POST['username']
        pass_ = request.POST['password']
        user = authenticate(request, username=check, password=pass_)
        if user is not None:
            login(request, user)
            # user is authenticated
            return redirect('/')
        else:
            return redirect('/get_form')
    return render(request, 'learning_logs/login_form.html')

# User profile posts


def posts_(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            topic_count = topic.objects.filter(user=request.user.id)
            entry_set = entry.objects.filter(user=request.user)
            context = {
                'topics': entry_set,
                'user_name': request.session['user_name'],
                'post_count': topic_count.count(),
            }
            return render(request, 'learning_logs/dashboard.html', context)
    else:
        return redirect('/login')


@csrf_exempt
def add_page(request):
    if request.user.is_authenticated:

        if request.method == 'GET':
            context = {
                'choices': Category.objects.all(),
            }

        if request.method == 'POST':
            topic_n = request.POST['topic_name']
            cat_ = Category.objects.filter(name=topic_n)
            topic_det = request.POST['text']
            picture = request.FILES['picture']

            top = topic(
                user=request.user, article_name=cat_[0])
            top.save()
            entery = entry.objects.create(
                user=request.user, topic=top, text=topic_det, picture=picture)

            entery.save()
            return redirect('/dashboard')

        return render(request, 'learning_logs/add_page.html', context)


@csrf_exempt
def update_post(request, topic_id):
    if request.method == "GET":
        topic_ini = topic.objects.get(id=topic_id)
        context = {
            'topic': topic_ini,
            'text': entry.objects.get(topic=topic_ini).text,
        }
        return render(request, 'learning_logs/add_page.html', context)

    elif request.method == 'POST':
        topic_ini = topic.objects.get(id=topic_id)
        new_entry = entry.objects.get(topic__id=topic_id)
        topic_ini.article_name = request.POST['topic_name']
        topic_ini.save()
        new_entry.text = request.POST['text']
        new_entry.save()
    return redirect('/dashboard')


def log_out(request):
    logout(request)
    return redirect('/login')


@csrf_exempt
def comment_add(request, entry_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            entry_ins = entry.objects.get(id=entry_id)
            text = request.POST['text']
            comment_entry = Comment(
                user=request.user, post=entry_ins, text=text)
            comment_entry.save()

            return redirect('/dashboard')
    return render(request, 'learning_logs/comment.html', {
        'id': entry_id
    })


def all_likes(request, entry_id):
    if request.method == 'GET':
        p = entry.objects.get(id=entry_id)
        number_of_likes = p.likes_set.all().count()
    return render(request, 'learning_logs/topic.html', {
        'number': number_of_likes
    })


def add_like(request, entry_id):
    if request.method == 'GET':
        entry_ins = entry.objects.get(id=entry_id)
        new_like, created = likes.objects.get_or_create(
            user=request.user, post=entry_ins)
        if not created:
            # the user already liked this picture before then delete (unlike the post)
            likes.objects.filter(user=request.user, post=entry_ins).delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def get_categories(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        context = {
            'categories': categories,
        }
        return render(request, 'learning_logs/categories.html', context)


def send_email(request):

    sub = Subscriber.objects.all()
    message = Mail(
        from_email='atifshafi63@gmail.com',
        to_emails=sub[0].email,
        subject='Newsletter Confirmation',
        html_content='Thank you for signing up for my email newsletter! \
                               Please complete the process by \
                               <a href="{}/confirm/?email={}&conf_num={}"> clicking here to \
                               confirm your registration</a>.'.format(request.build_absolute_uri('/confirm/'),
                                                                      sub[0].email,
                                                                      sub[0].conf_num))

    sg = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
    response = sg.send(message)

    return render(request, 'learning_logs/base.html')


def about_me(request):
    if request.method == "GET":
        return render(request, 'learning_logs/about.html')
