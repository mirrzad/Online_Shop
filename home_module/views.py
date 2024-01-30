from django.db.models import Sum
from django.shortcuts import render
from django.views.generic import TemplateView

from product_module.models import Product, ProductCategory
from site_module.models import SiteSettings, FooterLinkCategory, Slider
from utils.convertors import group_list


class HomeView(TemplateView):
    template_name = 'home_module/index_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slider_data = Slider.objects.filter(is_active=True)
        context['sliders'] = slider_data
        new_products = Product.objects.filter(is_active=True, is_delete=False).order_by('-id')[:8]
        context['product_list'] = group_list(new_products)
        most_view_products = Product.objects.filter(is_active=True, is_delete=False).order_by('-visits')[:8]
        context['most_view_products'] = group_list(most_view_products)
        categories = list(
            ProductCategory.objects.prefetch_related('products').filter(is_active=True, is_delete=False)[:6])
        category_list = []
        for category in categories:
            item = {
                'id': category.id,
                'title': category.title,
                'products': category.products
            }
            category_list.append(item)
        context['categories'] = category_list
        best_selling_products = Product.objects.filter(
            productorders__order__is_paid=True).annotate(
            order_count=Sum('productorders__count')).order_by('-order_count')[:8]
        context['best_selling_products'] = group_list(best_selling_products)
        return context


def site_header_component(request):
    settings = SiteSettings.objects.filter(is_main_setting=True).first()
    context = {'settings': settings}
    return render(request, 'shared/site_header_component.html', context)


def site_footer_component(request):
    settings = SiteSettings.objects.filter(is_main_setting=True).first()
    footer_link_cat = FooterLinkCategory.objects.all()
    context = {'settings': settings, 'footer_link_cat': footer_link_cat}
    return render(request, 'shared/site_footer_component.html', context)


class AboutUsView(TemplateView):
    template_name = 'home_module/about_us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        settings = SiteSettings.objects.filter(is_main_setting=True).first()
        context['settings'] = settings
        return context
