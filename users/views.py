from django.shortcuts import render, redirect, get_object_or_404

from django.http import JsonResponse
from .models import *
from .forms import OrderForm
from django.contrib.auth.models import User


from .tasks import send_mailing

def basket_adding(request):
    
    session_key = request.session.session_key
    data = request.POST

    product_id = data.get("product_id")
    product_remove = data.get("remove")
    nmb = data.get('product_num')

    if product_remove == 'true':
        product = ProductInBasket.objects.get(id=product_id, session_key=session_key)
        product.delete()

    elif product_remove == 'false':
        img = data.get('image')
        image = img[7:]

        if ProductInBasket.objects.filter(session_key=session_key, id=product_id):
            product = ProductInBasket.objects.get(session_key=session_key, id=product_id)
            product.nmb = int(nmb)
            product.save(force_update=True)

        else:
            new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id,
                                                                         defaults={"nmb": int(nmb), "poster": image})
            if not created:
                new_product.nmb = int(nmb)
                new_product.save(force_update=True)

    products_in_basket = ProductInBasket.objects.filter(session_key=session_key)
    products_total_nmb = products_in_basket.count()
    
    return_dict = dict()
    return_dict["products_total_nmb"] = products_total_nmb
    return_dict["products"] = list()

    product_total_sum = 0 
    for item in products_in_basket:
        product_dict = dict()
        product_dict["id"] = item.id
        product_dict["name"] = item.product.title
        product_dict["price"] = item.price_per_item
        product_dict["numbers"] = item.nmb
        product_dict["sum"] = item.total_price
        product_total_sum += item.total_price
        product_dict["img"] = item.poster.url
        product_dict["url"] = item.product.get_absolute_url()
        return_dict["products"].append(product_dict)

    return_dict["products_total_sum"] = product_total_sum
    return JsonResponse(return_dict)



def basket(request):
    """Список продуктов"""
    session_key = request.session.session_key
    data = request.POST
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key)

    context = {"product_list": products_in_basket,}

    return render(request, "product/basket_detail.html", context)


def likes(request):
    """Список продуктов"""
    session_key = request.session.session_key
    data = request.POST
    products_in_likes = ProductInLikes.objects.filter(session_key=session_key)

    context = {"product_list": products_in_likes,}

    return render(request, "product/likes.html", context)


def product_likes(request):
    session_key = request.session.session_key
    data = request.POST
    print(data)

    product_id = data.get("product_id")
    product_remove = data.get("remove")

    if product_remove == 'true':
        product = ProductInLikes.objects.get(id=product_id, session_key=session_key)
        product.delete()

    elif product_remove == 'false':

        if ProductInLikes.objects.filter(session_key=session_key, id=product_id):
            product = ProductInLikes.objects.get(session_key=session_key, id=product_id)
            product.save(force_update=True)

        else:
            new_product, created = ProductInLikes.objects.get_or_create(session_key=session_key, product_id=product_id)
            if not created:
                new_product.save(force_update=True)

    products_in_likes = ProductInLikes.objects.filter(session_key=session_key)
    products_likes_nmb = products_in_likes.count()
    
    return_dict = dict()
    return_dict["products_likes_nmb"] = products_likes_nmb
    
    return JsonResponse(return_dict)



def checkout(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key)
    
    order_sum = 0  
    for product in products_in_basket:
        order_sum += product.total_price
        
    form = OrderForm(request.POST)
    print(request.POST)

    if form.is_valid():
        print("form valide")
        data = request.POST
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        email = data.get('email')
        city = data.get('city')
        phone = data.get('phone')
        
        # # create user
        user, created = User.objects.get_or_create(username=phone, defaults={'first_name':firstname})
        # # создаем заказ
        order = Order.objects.create(user=user, firstname=firstname, lastname=lastname,
                                     email=email, city=city, phone=phone, status_id=1)
        order_id = order.id

        order_sum = 0
        # add in order
        for product in products_in_basket:
            
            ProductInOrder.objects.create(order=order, product=product.product, nmb=product.nmb, 
                                          price_per_item=product.price_per_item,
                                          total_price = product.total_price)
            order_sum += product.total_price
        # order send email
        send_mailing.delay(order_id)


        # clear basket
        # for item_clear in products_in_basket:
        #     item_clear.delete()

        context = {"order": order_id}

        return render(request, "product/order_accepted.html", context)
        

    else:
        print("form invalide")

    return render(request, "product/checkout.html", locals())