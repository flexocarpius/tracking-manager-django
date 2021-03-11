from django.shortcuts import render
from django.http import HttpResponseRedirect
from service.database.uow import UnitOfWork


uow = UnitOfWork()


def index(request):
    products = uow.products.all()
    return render(request, 'home/index.html', {'products': products})
