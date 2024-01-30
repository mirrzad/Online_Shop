from django.http import Http404, HttpRequest
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from account_module.models import User
from site_module.models import SiteBanner
from utils.convertors import group_list
from utils.http_service import get_client_ip
from .models import Product, ProductCategory, ProductBrand, ProductVisit, ProductGallery


class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'products'
    ordering = ['price']
    paginate_by = 3

    def get_queryset(self):
        query = super().get_queryset()
        cat_name = self.kwargs.get('category')
        brand_name = self.kwargs.get('br')
        request: HttpRequest = self.request
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')
        if start_price is not None:
            query = query.filter(price__gte=start_price)
        if end_price is not None:
            query = query.filter(price__lte=end_price)

        if cat_name is None and brand_name is None:
            query = query.filter(is_active=True)

        elif cat_name:
            query = query.filter(category__url_title__iexact=cat_name, is_active=True)

        elif brand_name:
            query = query.filter(brand__url_title__iexact=brand_name, is_active=True)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        request: HttpRequest = self.request
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')
        max_price = Product.objects.all().order_by('price').last().price
        context['start_price'] = start_price or 0
        context['end_price'] = end_price or max_price
        context['max_price'] = max_price
        banners = SiteBanner.objects.filter(
            is_active=True, position__iexact=SiteBanner.SiteBannerPosition.product_list)
        context['banners'] = banners
        return context


def product_category_component(request):
    categories = ProductCategory.objects.filter(is_active=True, is_delete=False)
    context = {'categories': categories}
    return render(request, 'product_module/components/product_category_component.html', context)


def product_brand_component(request):
    brands = ProductBrand.objects.prefetch_related('product_set').filter(is_active=True)
    context = {'brands': brands}
    return render(request, 'product_module/components/product_brand_component.html', context)


class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        banners = SiteBanner.objects.filter(
            is_active=True, position__iexact=SiteBanner.SiteBannerPosition.product_detail)
        context['banners'] = banners
        context['product_galleries'] = group_list(
            list(ProductGallery.objects.filter(product_id=self.object.id).all()), 3)
        related_products = list(Product.objects.filter(
            brand_id=self.object.brand_id).exclude(id=self.object.id).all()[:12])
        context['related_products'] = group_list(related_products, 3)
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id=self.object.id).exists()
        if not has_been_visited:
            new_visit = ProductVisit(user_id=user_id, ip=user_ip, product_id=self.object.id)
            new_visit.save()
        return context
