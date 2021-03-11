from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from service.database.uow import UnitOfWork
from service.models import UserRole
from .forms import UserForm, UserEditForm


uow = UnitOfWork()
active = 'admin_users'


def index(request):
    roles = uow.user_roles.all()
    return render(request, 'users/index.html', {'roles': roles, 'active': active})


def register(request, user_id=0):
    if request.method == 'POST':
        if request.POST['user_id']:
            form = UserEditForm(request.POST)
            if form.is_valid():
                role = uow.user_roles.get_by(user__id=request.POST['user_id'])
                role.user.username = form.data['username']
                role.user.email = form.data['email']
                role.role = form.data['role']
                uow.user_roles.update(role)
                uow.users.update(role.user)
                return HttpResponseRedirect('/users/')
            else:
                return render(request, 'users/register.html', {'errors': form.errors, 'active': active})
        else:
            form = UserForm(request.POST)
            if form.is_valid():
                # Adding user
                user = User.objects.create_user(
                    username=form.data['username'], email=form.data['email'], password=form.data['password'])
                uow.users.add(user)

                # Creating new role for user
                role = UserRole()
                role.user = user
                role.state = 'Active'
                role.role = form.data['role']
                uow.user_roles.add(role)
                return HttpResponseRedirect('/users/')
            else:
                return render(request, 'users/register.html', {'errors': form.errors, 'active': active})

    role = None
    if int(user_id) > 0:
        role = uow.user_roles.get_by(user__id=user_id)

    return render(request, 'users/register.html', {'role': role, 'active': active})
