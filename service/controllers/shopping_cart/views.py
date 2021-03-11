from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from service.database.uow import UnitOfWork


uow = UnitOfWork()


def index(request):
    context = {'products': list(uow.products.all())}
    return render(request, 'shopping_cart/index.html', context)
