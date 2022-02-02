from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),

    path("category/", views.CategoryListView.as_view(), name="category_list"),
    path("category/<str:category>/", views.ProductView.as_view(), name="product_list"),
    path("category/<str:category>/<str:slug>/", views.ProductDetailView.as_view(), name="product_detail"),

    path('new/', views.NewProductAll.as_view(), name="all_new"),
    path('new/<slug:date>/', views.NewProductDay.as_view(), name="day_new"),

    path("add-rating/", views.add_star_rating, name='add_rating'),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    path("search/", views.Search.as_view(), name="search"),
]


# handler404 = 'product.views.handler404'
# handler500 = 'my_app.views.handler500'