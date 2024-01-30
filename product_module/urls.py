from django.urls import path
from . import views
urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('category/<str:category>', views.ProductListView.as_view(), name='product_by_category_list'),
    path('brand/<str:br>', views.ProductListView.as_view(), name='product_by_brand_list'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product_detail'),
]
