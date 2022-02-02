from django.urls import path
from . import views

urlpatterns = [
    path("basket_adding/", views.basket_adding, name="basket_adding"),
    path("basket/", views.basket, name="basket"),
    path("likes_adding/", views.product_likes, name="product_likes"),
    path("likes/", views.likes, name="likes"),
    path("checkout/", views.checkout, name="checkout"),
]