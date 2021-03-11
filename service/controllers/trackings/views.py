import json
import datetime
from django.http import JsonResponse
from django.shortcuts import render
from service.models import Tracking
from service.database.uow import UnitOfWork


uow = UnitOfWork()
active = 'admin_trackings'


def index(request):
    context = get_context(request)
    return render(request, 'trackings/index.html', context)


def details(request, tracking_id):
    tracking = uow.trackings.get(tracking_id).to_dict()

    if tracking['state'] == 'Placed':
        tracking['actions'] = ['Ship', 'Cancel', 'Delay']
    elif tracking['state'] == 'Shipped':
        tracking['actions'] = ['Deliver', 'Delay']
    elif tracking['state'] == 'Cancelled':
        tracking['actions'] = ['Send', 'Refund']

    return render(request, 'trackings/details.html', {'tracking': tracking, 'active': active})


def get_context(request):
    trackings = [tracking.to_dict()
                 for tracking in uow.trackings.all().order_by('id')]
    for tracking in trackings:
        if tracking['state'] == 'Placed':
            tracking['actions'] = ['Ship', 'Cancel', 'Delay']
        elif tracking['state'] == 'Shipped':
            tracking['actions'] = ['Deliver', 'Delay']
        elif tracking['state'] == 'Cancelled':
            tracking['actions'] = ['Send', 'Refund']
    return {'trackings': trackings, 'active': active}

#
# API calls
#


# GET
def trackings_order(request, order_id=0):
    if request.method == 'GET':
        context = get_context(request)
        return JsonResponse({'data': context['trackings']})


def trackings_process(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data.get('id', None) is not None and data.get('action', None) is not None:
            tracking = uow.trackings.get(data['id'])
            if data.get('action') == 'Ship':
                tracking.state = 'Shipped'
                tracking.shipped_date = datetime.date.today()
            elif data.get('action') == 'Cancel':
                tracking.state = 'Cancelled'
                tracking.cancelled_date = datetime.date.today()
            elif data.get('action') == 'Delay':
                tracking.state = 'Delayed'
                tracking.delayed_date = datetime.date.today()
            elif data.get('action') == 'Deliver':
                tracking.state = 'Delivered'
                tracking.delivered_date = datetime.date.today()
            elif data.get('action') == 'Refund':
                tracking.state = 'Refunded'
            elif data.get('action') == 'Send':
                tracking.state = 'Shipped'
                tracking.shipped_date = datetime.date.today()
            uow.trackings.update(tracking)
            return JsonResponse({'message': 'ok', 'data': tracking.to_dict()})
        else:
            return JsonResponse({'message': 'Missing parameters.'})
    else:
        return JsonResponse({'message': 'Invalid method.'})
