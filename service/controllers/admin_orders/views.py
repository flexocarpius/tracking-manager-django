import json
from django.http import JsonResponse
from django.shortcuts import render
from service.database.uow import UnitOfWork
from service.utils import states
from service.business.orders import OrdersBusiness


uow = UnitOfWork()
active = 'admin_orders'
business = OrdersBusiness()


def index(request):
    orders = [order.to_dict()
              for order in uow.orders.all()]
    for order in orders:
        order['trackings'] = uow.trackings.all_by(order__id=order['id'])
        order['actions'] = get_order_actions(order)
    return render(request, 'admin_orders/index.html', {'orders': orders, 'active': active})


def order_process(request):
    if request.user.is_authenticated and request.method == 'POST':
        role = uow.user_roles.get_by(user__id=request.user.id)
        if role.role in 'Admin' or role.role in 'Operator':
            action = request.POST['submit']
            order_id = request.POST['order_id']
            if action == states.ORDER_ACTIONS_FORCE_CANCEL:
                # Cancel everything, including trackings.
                order = uow.orders.get(order_id)
                trackings = list(uow.trackings.get_by(order__id=order_id))

                order.state = states.ORDER_CANCELLED
                uow.orders.update(order)

                for tracking in trackings:
                    tracking.state = states.TRACKINGS_CANCELLED
                    uow.trackings.update(tracking)

            if action == states.ORDER_ACTIONS_REFUND:
                # Process a refund
                order = uow.orders.get(order_id)
                trackings = list(uow.trackings.all_by(order__id=order_id))

                if business.refund_payment(order.payment_reference):
                    order.state = states.ORDER_REFUNDED
                    uow.orders.update(order)

                    for tracking in trackings:
                        tracking.state = states.TRACKINGS_REFUNDED
                        uow.trackings.update(tracking)

            if action == states.ORDER_ACTIONS_UPDATE_REFERENCE:
                # Find and old id to convert to a transaction id.
                order = uow.orders.get(order_id)

                transaction_id = business.get_transaction_from_capture(
                    order.payment_reference)
                order.payment_reference = transaction_id
                uow.orders.update(order)

    orders = [order.to_dict()
              for order in uow.orders.all()]
    for order in orders:
        order['trackings'] = uow.trackings.all_by(order__id=order['id'])
    return render(request, 'admin_orders/index.html', {'orders': orders, 'active': active})


def get_order_actions(order):
    actions = []

    if order['state'] == 'Creating':
        actions = ['Force Cancel']
    elif order['state'] == 'Placed':
        actions = ['Force Cancel']
    elif order['state'] == 'Paid':
        actions = ['Force Cancel']
    elif order['state'] == 'Requested Refund':
        actions = ['Refund']
    elif order['state'] == 'Cancelled' and order['payment_reference'] is not None:
        actions = ['Refund']

    if order['payment_reference'] is not None:
        actions.append('Update Reference')

    return actions


# API calls
def order_actions(request):
    data = json.loads(request.body)
    order_id = data['orderId']
    order = uow.orders.get(order_id).to_dict()
    actions = get_order_actions(order)

    return JsonResponse({'message': 'ok', 'data': actions})
