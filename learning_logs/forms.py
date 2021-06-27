from django import forms
from django.forms import ModelForm, fields
from django.forms.widgets import PasswordInput, Textarea
from django.contrib.auth.models import User


class MyForm(ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
    first_name = forms.TextInput(attrs={'class': 'form-control'})
    name = forms.TextInput(attrs={'class': 'form-control'})
    last_name = forms.TextInput(attrs={'class': 'form-control'})
    username = forms.TextInput(attrs={'class': 'form-control'})
    email = forms.TextInput(attrs={'class': 'form-control'})
    password = forms.TextInput(attrs={'class': 'form-control'})

    def __init__(self, *args, **kwargs):
        super(MyForm, self).__init__(*args, **kwargs)

        for fieldname in ['password', 'email', 'username']:
            self.fields[fieldname].help_text = None


class LoginForm(forms.Form):
    login = forms.CharField(max_length=250)
    password = forms.CharField(widget=PasswordInput)


class EditForm(forms.Form):
    topic_name = forms.CharField()
    topic_name.widget.attrs = {
        'class': 'form-control',
        'name': 'topicname'
    }
    text = forms.CharField(widget=forms.Textarea)
    text.widget.attrs = {

        'name': 'text'
    }
    text.widget.attrs = {
        'class': 'form-control',
        'cols': 40,
        'rows': 20
    }
