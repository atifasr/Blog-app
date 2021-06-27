
from django.shortcuts import render,redirect
from practice.models import blog_det
from practice.forms import Blog_entry,register_
from datetime import time,date
# Create your views here.

def index(request):
    date_ = date.today()
    time_ = time()
    context = {'date': date_,}
    return render(request,'practice/base.html',context)



def blog(request):
    blog_info = blog_det.objects.all()
    context = {'details':blog_info}
    return render(request,'practice/child1.html',context)

def entry(request):
    if request.method!='POST':
        form=Blog_entry()
    else:
        form=Blog_entry(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('practice:blog')

    context = {'form':form,'time':time,'date':date}
    return render(request,'practice/create_entry.html',context)


def register(request):
    if request.method!='POST':
        form = register_()
    else:
        form = register_(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('practice:blog')
    context = {'form':form}        
    return render(request,'practice/register.html',context)









