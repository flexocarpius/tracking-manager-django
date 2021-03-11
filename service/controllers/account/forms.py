from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='User name', max_length=200)
    password = forms.CharField(label='User password', max_length=300)
