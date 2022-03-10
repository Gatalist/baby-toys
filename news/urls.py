from django.urls import path
from . import views


urlpatterns = [
    path("", views.NewsView.as_view(), name="news"),
    path("<slug:slug>/", views.NewsDetailView.as_view(), name="news_detail"),
]
