from django import forms


class CreatForm(forms.Form):
    name = forms.CharField(max_length=255, label='Name', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'required': True,

    }))
    address = forms.CharField(max_length=255, label='address', widget=forms.TextInput(attrs={
        'class': 'form-control',
        'required': True,

    }))
