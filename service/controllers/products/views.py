import json
import pandas as pd
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from service.database.uow import UnitOfWork
from .forms import ProductForm
from service.models import Product, ProductGalleryImage


uow = UnitOfWork()
active = 'admin_products'


def index(request):
    context = {'products': list(uow.products.all()), 'active': active}
    return render(request, 'products/index.html', context)


def details(request, product_id):
    product = uow.products.get(product_id)
    trackings_product = uow.trackings.all_by(product__id=product_id)
    totals = [
        {
            'total': tp.quantity * tp.product.price,
            'count': tp.quantity,
            'price': tp.product.price
        }
        for tp in trackings_product
    ]
    indices = [tp.product.name for tp in trackings_product]
    trackings_df = pd.DataFrame(
        data=totals,
        index=indices
    )

    total = 0
    count = 0

    if product and len(trackings_product) > 0:
        total = trackings_df.sum(axis=0)[0]
        count = trackings_df.count()[0]

    return render(request, 'products/details.html',
                  {
                      'product': product,
                      'total': total,
                      'count': count,
                      'active': active
                  }
                  )


def create(request, product_id=0):
    if request.method == 'GET':
        if product_id:
            product = uow.products.get(product_id)
            return render(request, 'products/create.html', {'product': product, 'active': active})
        else:
            return render(request, 'products/create.html', {'active': active})
    elif request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            entity = None
            if form.data.get('product_id', '0') != '':
                entity = uow.products.get(form.data['product_id'])
                entity.name = form.data['name']
                entity.description = form.data['description']
                entity.price = form.data['price']
                entity.quantity = form.data['quantity']
                entity.small_img = form.data['small_img']
                entity.large_img = form.data['large_img']
                uow.products.update(entity)
            else:
                entity = Product(
                    name=form.data['name'],
                    description=form.data['description'],
                    price=form.data['price'],
                    quantity=form.data['quantity'],
                    small_img=form.data['small_img'],
                    large_img=form.data['large_img'],
                )
                uow.products.add(entity)
            return HttpResponseRedirect('/products/')
        else:
            if product_id:
                product = uow.products.get(product_id)
                return render(request, 'products/create.html', {'product': product, 'errors': form.errors, 'active': active})
            else:
                return render(request, 'products/create.html', {'errors': form.errors, 'active': active})


def gallery(request, product_id):
    product = uow.products.get(product_id)
    return render(request, 'products/gallery.html', {'product': product, 'active': active})


# API calls
# GET /products/details/data/id
def details_insights(request, product_id):
    trackings_product = uow.trackings.all_by(product__id=product_id)
    totals = [tp.quantity * tp.product.price for tp in trackings_product]
    trackings = [tp.name for tp in trackings_product]
    return JsonResponse({
        'totals': totals,
        'trackings': trackings
    })


# POST /products/create/gallery
def add_gallery_image(request, product_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        product = uow.products.get(product_id)
        if data['url'] is not None and product is not None:
            product_img = ProductGalleryImage(
                product=product,
                img_url=data['url']
            )
            uow.product_images.add(product_img)
        else:
            return JsonResponse({'message': 'Url not present or product does not exist.'})
        return JsonResponse({'message': 'ok', 'data': product_img.to_dict()})
    elif request.method == 'GET':
        product_imgs = [product_img.to_dict(
        ) for product_img in uow.product_images.all_by(product__id=product_id)]
        return JsonResponse({'data': product_imgs})


def remove_gallery_image(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_image_id = data['id']
        product_image = uow.product_images.get(product_image_id)
        if product_image is not None:
            uow.product_images.remove(product_image)
            return JsonResponse({'message': 'ok'})
        else:
            return JsonResponse({'message': 'Product image does not exist.'})
    elif request.method == 'GET':
        return JsonResponse({'message': 'Invalid method.'})


def product_search(request):
    query = request.GET.get('q')
    if len(query) > 0:
        products = [product.to_dict()
                    for product in uow.products.all_by(name__icontains=query)]
        return JsonResponse({'message': 'ok', 'data': products})
    else:
        return JsonResponse({'message': 'ok', 'data': '[]'})
