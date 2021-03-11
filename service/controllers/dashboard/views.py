import datetime
import calendar
import random
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Sum, Count
from service.database.uow import UnitOfWork
from service.utils import states


EARNING_GOAL = 1000.0


uow = UnitOfWork()
active = 'admin_dashboard'


def index(request):
    today = datetime.date.today()

    orders_month = uow.orders.all_by(
        payment_date__year=today.year,
        payment_date__month=today.month
    )

    startdate = today - datetime.timedelta(days=today.weekday())
    enddate = startdate + datetime.timedelta(days=6)

    orders_week = uow.orders.all_by(
        payment_date__gte=startdate,
        payment_date__lte=enddate
    )

    month_total = sum([order.total for order in orders_month])
    week_total = sum([order.total for order in orders_week])
    orders_for_refund = list(uow.orders.all_by(
        state=states.ORDER_REQUESTED_REFUND))

    # Test
    week_total = 3345.15
    month_total = 125728.48

    return render(request, 'dashboard/index.html', {
        'orders_week': orders_week,
        'orders_month': orders_month,
        'orders_for_refund': orders_for_refund,
        'month_total': month_total,
        'week_total': week_total,
        'active': active,
    })


# API calls


def total_progress(request):
    today = datetime.date.today()
    orders_month = uow.orders.all_by(
        payment_date__year=today.year,
        payment_date__month=today.month
    )
    month_total = sum([order.total for order in orders_month])
    progress = (month_total / EARNING_GOAL) * 100

    # Test
    progress = 120
    return JsonResponse({'message': 'ok', 'data': progress})


def week_earnings_day(request):
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    today = datetime.date.today()
    dt = datetime.date.today() - datetime.timedelta(days=today.weekday())

    day_earnings = {}

    for day in days:
        orders_day = uow.orders.all_by(
            payment_date__year=dt.year,
            payment_date__month=dt.month,
            payment_date__day=dt.day,
        )
        day_earnings[day] = sum([order.total for order in orders_day])
        dt = dt + datetime.timedelta(days=1)

    # Test data
    for day in days:
        day_earnings[day] = random.randint(10, 100)

    return JsonResponse({'message': 'ok', 'data': day_earnings})


def get_featured_products(request):
    featured = uow.trackings.objects.values('product__id', 'product__name', 'product__small_img') \
        .annotate(Sum('quantity')) \
        .order_by('-quantity__sum')[:5]
    featured_list = list(featured)
    featured_response = [
        {
            'id': featured['product__id'],
            'product': featured['product__name'],
            'quantity': featured['quantity__sum'],
            'small_img': featured['product__small_img'],
        }
        for featured in featured_list]
    return JsonResponse({'message': 'ok', 'data': featured_response})


def orders_state(request):
    states = [state[0] for state in list(
        uow.orders.objects.order_by().values_list('state').distinct())]
    states_response = []
    for state in states:
        count = uow.orders.all_by(state=state).count()
        states_response.append({'state': state, 'count': count})
    return JsonResponse({'message': 'ok', 'data': states_response})
