
from django import forms
from .models import blog_det,user_info
from django.utils.translation import gettext_lazy as _



class Blog_entry(forms.ModelForm):
    class Meta:
        model = blog_det
        fields = ('blog_name','text')
        labels = {
            'blog_name': _('enter sweety'),
        }


class register_(forms.ModelForm):
   
    class Meta:
        model = user_info
        fields = ('user_id','first_name','designation','password')
        label = {
            'user_id':_('enter the user id'),
            'password':_('authentication key'),
        }


        







