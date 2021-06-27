from django.shortcuts import redirect, render

from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Count
from .models import topic, entry, Comment,likes ,Category
from .forms import MyForm, LoginForm, EditForm
from django.views.decorators.csrf import csrf_exempt
from .models import topic, entry
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User



# Home page / Base template
def index(request):
    entries_ = entry.objects.all().order_by('date_added')


    if request.method == 'GET':
        if request.user.is_authenticated:
            request.session['user_name'] = request.user.get_short_name()
            request.session['logged_in'] = True
        else:
            request.session['user_name'] = None
            request.session['logged_in'] = False
        return render(request, 'learning_logs/base.html', {'user':  request.session['user_name'],
                                                            'entries': entries_,
                                                            'logged_in' :request.session['logged_in'], })



# Topics views
def topics(request):
    if request.user.is_authenticated:
        if request.method=="GET":
            topics = topic.objects.filter(
                user__id=request.user.id).annotate(dcount=Count('article_name')).order_by('date_added')

            # entry_set = entry.objects.filter(user__id = request.user)

            context = {'topics': topics}
            return render(request, 'learning_logs/topics.html', context)
    else:
        return redirect('/login')



def posts_(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            # topic_id = topic.objects.get(user=request.user)

            entry_set = entry.objects.filter(user=request.user)
            context = {'topics': entry_set,
                       'user_name': request.session['user_name'],}
            return render(request, 'learning_logs/dashboard.html', context)



# Getting entry by topic id
def topic_a(request, art_name):
    #show single topics
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
        new_frm = MyForm(request.POST)
        if new_frm.is_valid():
            fname = new_frm.cleaned_data['first_name']
            lname = new_frm.cleaned_data['last_name']
            uname = new_frm.cleaned_data['username']
            email_add = new_frm.cleaned_data['email']
            password = new_frm.cleaned_data['password']
            new_user = User.objects.create_user(first_name=fname, last_name=lname,
                                                username=uname, email=email_add, password=password)
            new_user.save()
        return HttpResponseRedirect('/login')

    else:
        new_frm = MyForm(initial={
            'firstname': '',
            'lastname': '',
            'username': '',
            'email': '',
            'password': '', })
    context = {
        'form': new_frm,
    }
    return render(request, 'learning_logs/data_form.html', context)

# login form


@csrf_exempt
def login_form(request):
    # login form
    login_frm = LoginForm()
    if request.method == 'POST':
        login_frm = LoginForm(request.POST)
        if login_frm.is_valid():
            check = login_frm.cleaned_data['login']
            pass_ = login_frm.cleaned_data['password']
            user = authenticate(request, username=check, password=pass_)
            if user is not None:
                login(request, user)
               # user is authenticated
                return redirect('/dashboard')
            else:
                return redirect('/get_form')
    context = {
        'form': login_frm,
    }
    return render(request, 'learning_logs/login_form.html', context)


def dashboard_(request):
    if request.user.is_authenticated:
        topic_count = topic.objects.filter(user__id=request.user.id)

        if request.method=='GET':
            return render(request, 'learning_logs/dashboard.html', {
                'user_name': request.session['user_name'],
                'post_count': topic_count.count()
            })
    else:
        return redirect('/login')


@csrf_exempt
def add_page(request):
    if request.user.is_authenticated:

        if request.method == 'GET':
            context = {
                'choices ': Category.objects.all(),
            }

        if request.method == 'POST':
            topic_n = request.POST['topic_name']
            topic_det = request.POST['text']
            picture= request.FILES['picture']
            top = topic(
                user=request.user, article_name=topic_n)
            top.save()
            entery = entry.objects.create(topic=top, text=topic_det)

            entery.save()
            return redirect('/dashboard')

        return render(request,'learning_logs/add_page.html',context)


@csrf_exempt
def update_post(request, topic_id):
    if request.method == "GET":
        topic_ini = topic.objects.get(id=topic_id)
        context = {
            'topic': topic_ini,
            'text': entry.objects.get(topic__id=topic_id).text,
        }
        # update_frm = EditForm(initial=data)
        return render(request, 'learning_logs/add_page.html', context)

    elif request.method=='POST':
        topic_ini = topic.objects.get(id=topic_id)
        new_entry = entry.objects.get(topic__id=topic_id)
        topic_ini.article_name=request.POST['topic_name']
        topic_ini.save()
        new_entry.text = request.POST['text']
        new_entry.save()
    return redirect('/dashboard')


def log_out(request):
    logout(request)
    return redirect('/login')

@csrf_exempt
def comment_add(request,entry_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            entry_ins=entry.objects.get(id=entry_id)
            text=request.POST['text']
            comment_entry=Comment(user=request.user,post = entry_ins,text=text)
            comment_entry.save()

            return redirect('/dashboard')
    return render(request, 'learning_logs/comment.html',{
        'id': entry_id
    })



def all_likes(request,entry_id):
    if request.method == 'GET':
        p = entry.objects.get(id=entry_id)
        number_of_likes = p.likes_set.all().count()
    return render(request,'learning_logs/topic.html',{
        'number':number_of_likes
    })

def add_like(request,entry_id):
    if request.method=='GET':
        entry_ins = entry.objects.get(id=entry_id)
        new_like, created = likes.objects.get_or_create(user=request.user, post=entry_ins)
        if not created:
            # the user already liked this picture before
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def get_categories(request):
    if request.method== 'GET':
        categories = Category.objects.all()
        context ={
            'categories' : categories,
        }
        return  render(request,'learning_logs/categories.html',context)

