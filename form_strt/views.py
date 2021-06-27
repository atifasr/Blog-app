
from os import name
from django import forms
from .forms import CreatForm

from django.shortcuts import redirect, render
# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from .models import TestData


def disp_(request):
    try:
        disp_test = TestData.objects.all().order_by('name')
    except TestData.DoesNotExist:
        disp_test = None
    context = {
        'data': disp_test
    }
    return render(request, 'form_strt/form.html', context)


@csrf_exempt
def create(request):
    my_frm = CreatForm()
    if request.method == 'POST':
        new_data = TestData()
        my_frm = CreatForm(request.POST)
        if my_frm.is_valid():
            new_data.name = my_frm.cleaned_data['name']
            new_data.address = my_frm.cleaned_data['address']
            new_data.save()
            return redirect('/')
    context = {
        'form': my_frm,
    }

    return render(request, 'form_strt/create.html', context)


@csrf_exempt
def update(request, val_id):
    """updating form"""
    up_frm = CreatForm()
    try:
        get_data = TestData.objects.filter(id=val_id)
        if request.method == 'POST':
            up_frm = CreatForm(request.POST, instance=get_data)
            if up_frm.is_valid():
                up_frm.save()
                return redirect('/')
            else:
                up_frm = CreatForm(instance=get_data)
    except TestData.DoesNotExist:
        return redirect('/')
    context = {
        'form': up_frm
    }
    return render(request, 'form_strt/update.html', context)


def delete_(request, val_id):
    try:
        TestData.objects.filter(id=val_id).delete()
    except TestData.DoesNotExist:
        return redirect('create/')
    return redirect('/')


# def disp_data(request):
#     try:
#         disp_test = TestData.objects.all()
#     except TestData.DoesNotExist:
#         return redirect('/create')

#     return render(request, 'form_strt/form.html')
