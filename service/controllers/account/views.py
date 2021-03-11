from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from .forms import LoginForm
from service.database.uow import UnitOfWork
from service.models import UserRole


uow = UnitOfWork()


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.data['username']
            password = form.data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                # Correct password, and the user is marked "active"
                role = uow.user_roles.get_by(user__id=user.id)

                # If no roles exist for the user, create
                if role is None:
                    role = UserRole(user=user, state='Active', role='Admin')
                    uow.user_roles.add(role)

                # Update the role property in the session
                request.session['role'] = role.role
                auth.login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect('/')
            else:
                # Show an error page
                return HttpResponseRedirect('/account')
        else:
            return render(request, 'account/index.html', {'errors': form.errors})
    return render(request, 'account/index.html')


def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect('/')
