from django import forms


class UserForm(forms.Form):
    username = forms.CharField(label='User name', max_length=100)
    email = forms.CharField(label='User email', max_length=200)
    role = forms.CharField(label='User role', max_length=100)
    password = forms.CharField(label='User password', max_length=300)


class UserEditForm(forms.Form):
    user_id = forms.IntegerField()
    username = forms.CharField(label='User name', max_length=100)
    email = forms.CharField(label='User email', max_length=200)
    role = forms.CharField(label='User role', max_length=100)
