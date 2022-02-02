from .models import ProductInBasket, ProductInLikes


def getting_basket_info(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.cycle_key()

    products_in_basket = ProductInBasket.objects.filter(session_key=session_key)
    products_total_nmb = products_in_basket.count()

    products_in_likes = ProductInLikes.objects.filter(session_key=session_key)
    products_likes_nmb = products_in_likes.count()

    products_total_sum = 0
    for sum_product in products_in_basket:
       products_total_sum += sum_product.total_price

    return locals()