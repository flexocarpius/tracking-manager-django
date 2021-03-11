import datetime
import json
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from service.database.uow import UnitOfWork
from service.models import Order, Tracking
from .forms import OrderForm
from service.business.orders import OrdersBusiness


uow = UnitOfWork()
business = OrdersBusiness()


def index(request):
    if request.user is not None:
        orders = [order.to_dict()
                  for order in uow.orders.all_by(user__id=request.user.id)]
        for order in orders:
            order['trackings'] = uow.trackings.all_by(order__id=order['id'])
            if order['state'] == 'Creating':
                order['actions'] = ['Cancel']
            elif order['state'] == 'Placed':
                order['actions'] = ['Cancel']
            elif order['state'] == 'Paid':
                order['actions'] = ['Cancel', 'Refund']
        return render(request, 'orders/index.html', {'orders': orders, 'active': 'orders'})
    else:
        return HttpResponseRedirect('/account/login')


def details(request, order_id):
    order = uow.orders.get(order_id).to_dict()
    trackings = [trackings.to_dict()
                 for trackings in uow.trackings.all_by(order__id=order['id'])]
    for tracking in trackings:
        tracking['subtotal'] = tracking['product']['price'] * \
            tracking['quantity']
    payment_valid = business.is_payment_valid(
        order['total'], order['payment_reference'])

    # Add available actions for admins and operators
    if (request.session['role'] in 'Admin' or request.session['role'] in 'Operator'):
        if order['state'] == 'Creating':
            order['actions'] = ['Force Cancel']
        elif order['state'] == 'Placed':
            order['actions'] = ['Force Cancel']
        elif order['state'] == 'Paid':
            order['actions'] = ['Force Cancel']
        elif order['state'] == 'Requested Refund':
            order['actions'] = ['Refund']
        elif order['state'] == 'Cancelled' and order['payment_reference'] is not None:
            order['actions'] = ['Refund']

        if order['payment_reference'] is not None and order['state'] not in 'Refunded':
            if order.get('actions', None) is None:
                order['actions'] = []
            order['actions'].append('Update Reference')

    return render(request, 'orders/details.html', {'order': order, 'trackings': trackings, 'active': 'orders', 'payment_valid': payment_valid})


def create(request):
    # obtain_order_context will create an order in case it does not exists.
    context = obtain_order_context(request)
    context['order'] = uow.orders.get_by(
        state='Creating', user__id=request.user.id)
    context['active'] = 'checkout'
    return render(request, 'orders/create.html', context)


def product_details(request, product_id):
    product = uow.products.get(product_id)
    product_imgs = uow.product_images.all_by(product__id=product.id)
    buy_count = len(uow.trackings.all_by(product__id=product_id))
    return render(request, 'orders/view_product.html', {'product': product, 'buy_count': buy_count, 'product_imgs': product_imgs})


def place_order(request):
    context = obtain_order_context(request)
    order = uow.orders.get_by(state='Creating', user__id=request.user.id)
    context['order'] = order
    context['active'] = 'checkout'

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid() and order.id == int(form.data['order_id']):
            order.shipping_address = form.data['shipping_address']
            order.placed_date = datetime.date.today()
            uow.orders.update(order)
            return render(request, 'orders/place.html', context)
        else:
            return render(request, 'orders/place.html', context)
    else:
        return render(request, 'orders/place.html', context)


def order_placed(request):
    order_id = request.session.get('order_id', None)

    if order_id is None:
        return render(request, 'shared/error.html', {'active': 'checkout'})

    order = uow.orders.get(order_id)
    if order is None:
        return render(request, 'shared/error.html', {'active': 'checkout'})

    if order.state == 'Paid':
        del request.session['order_id']
        return render(request, 'orders/success.html', {'order': order, 'active': 'checkout'})
    else:
        return render(request, 'shared/error.html', {'active': 'checkout'})


def obtain_order_context(request):
    order = uow.orders.get_by(state='Creating', user__id=request.user.id)

    # Create order if it does no exist
    if order is None:
        order = Order()
        order.user = request.user
        order.shipping_address = ''
        order.state = 'Creating'
        uow.orders.add(order)

        # Assign a code to this order
        order.code = Order.generate_code(order.id)
        order.created_date = datetime.date.today()
        uow.orders.update(order)

    trackings = uow.trackings.all_by(order__id=order.id)
    products = [tracking.product.to_dict() for tracking in trackings]
    total = 0.0

    for tracking in trackings:
        product = next((p for p in products if p['id'] ==
                        tracking.product.id), None)
        if product is not None:
            product['to_buy'] = tracking.quantity
            total += product['to_buy'] * product['price']
            product['subtotal'] = product['to_buy'] * product['price']

    return {
        'products': products,
        'total': float('{0:10.2f}'.format(total)),
        'total_products': len(products),
        'trackings': [tracking.to_dict() for tracking in trackings],
        'active': 'orders'
    }


"""
API Calls
"""

# POST /orders/process


def set_order_placed(request):
    data = json.loads(request.body)
    context = obtain_order_context(request)
    order = uow.orders.get_by(state='Creating', user__id=request.user.id)

    if request.method == 'POST':
        # Validate payment with PayPal
        if not business.is_order_valid(context['total'], data.get('id', '')):
            return JsonResponse({'message': 'Invalid payment'})

        order.state = 'Paid'
        order.payment_reference = business.get_transaction_from_capture(
            data.get('id', None))
        order.total = context['total']
        order.payment_date = datetime.date.today()
        uow.orders.update(order)

        # Update trackings for each item in the cart
        for tracking in context.get('trackings', []):
            tracking_db = uow.trackings.get(tracking['id'])
            tracking_db.state = 'Placed'
            tracking_db.placed_date = datetime.date.today()
            uow.trackings.update(tracking_db)

            # Remove from inventory
            product = uow.products.get(tracking_db.product.id)
            product.quantity -= tracking_db.quantity
            uow.products.update(product)

        # Adding session to make the result available for the user
        request.session['order_id'] = order.id
        request.session.modified = True

        return JsonResponse({'message': 'ok'})

    return JsonResponse({'message': 'Invalid method'})


# POST /orders/product
def add_product(request):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'login'})

    data = json.loads(request.body)
    product_id = int(data.get('productId', '0'))
    quantity = int(data.get('quantity', '0'))

    if not request.user.is_authenticated:
        return HttpResponseRedirect('/account/login')

    product = uow.products.get(product_id)
    order = uow.orders.get_by(state='Creating', user__id=request.user.id)
    trackings = list(uow.trackings.all_by(order__id=order.id))
    products = [tracking.product for tracking in trackings]
    products_id = [product.id for product in products]

    # Validate if product exists
    if product is None:
        return JsonResponse({'message': 'Product does not exist'})

    # Validate if quantity is on product inventory
    if quantity > 0 and quantity > product.quantity:
        return JsonResponse({'message': 'Not enough inventory'})

    # Add normally
    if product_id not in products_id:
        tracking = Tracking(
            name=Tracking.generate_code(product_id),
            description='',
            quantity=quantity,
            state='Creating',
            product=product,
            order=order,
            created_date=datetime.date.today()
        )
        uow.trackings.add(tracking)
    else:
        return JsonResponse({'message': 'Already added'})
    return JsonResponse({'message': 'ok'})


def remove_product(request):
    data = json.loads(request.body)
    order_id = int(data.get('orderId', None))
    product_id = int(data.get('productId', None))
    if order_id is not None and product_id is not None:
        tracking = uow.trackings.get_by(
            order__id=order_id, product__id=product_id)
        if tracking:
            uow.trackings.remove(tracking)
            return JsonResponse({'message': 'ok', 'data': tracking.to_dict()})
        else:
            return JsonResponse({'message': 'Tracking not found.'})
    else:
        return JsonResponse({'message': 'Invalid parameters.'})


def get_products(request):
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'login'})

    context = obtain_order_context(request)
    return JsonResponse({'message': 'ok', 'data': context})


def cancel_order(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        context = obtain_order_context(request)
        order = uow.orders.get(data['id'])
        if order is None:
            return JsonResponse({'message': 'Order not found.'})

        # Cancel order and all its trackings
        if order.state == 'Cancelled':
            return JsonResponse({'message': 'Order has been already cancelled.'})

        order.state = 'Cancelled'
        order.cancelled_date = datetime.date.today()
        uow.orders.update(order)
        for track in context['trackings']:
            tracking = uow.trackings.get(track['id'])
            tracking.state = 'Cancelled'
            tracking.cancelled_date = datetime.date.today()
            uow.trackings.update(tracking)

        return JsonResponse({'message': 'ok'})
    else:
        return JsonResponse({'message': 'Invalid method.'})


def request_order_refund(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        context = obtain_order_context(request)
        order = uow.orders.get(data['id'])
        if order is None:
            return JsonResponse({'message': 'Order not found.'})

        # Cancel order and all its trackings
        if order.state == 'Refund':
            return JsonResponse({'message': 'Order has been already refunded.'})

        if order.state == 'Requested Refund':
            return JsonResponse({'message': 'Already requested for refund.'})

        order.state = 'Requested Refund'
        uow.orders.update(order)

        return JsonResponse({'message': 'ok'})
    else:
        return JsonResponse({'message': 'Invalid method.'})


def order_actions(request):
    data = json.loads(request.body)
    order_id = data['orderId']
    order = uow.orders.get(order_id)

    if order['state'] == 'Creating':
        order['actions'] = ['Force Cancel']
    elif order['state'] == 'Placed':
        order['actions'] = ['Force Cancel']
    elif order['state'] == 'Paid':
        order['actions'] = ['Force Cancel']
    elif order['state'] == 'Requested Refund':
        order['actions'] = ['Refund']
    elif order['state'] == 'Cancelled' and order['payment_reference'] is not None:
        order['actions'] = ['Refund']

    return JsonResponse({'message': 'ok', 'data': order['actions']})
