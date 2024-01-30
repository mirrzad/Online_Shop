from django.contrib import admin

from . import models


class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'footer_link_category']


class SliderAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'is_active']
    list_editable = ['is_active', 'url']


class SiteBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'position']


admin.site.register(models.SiteSettings)
admin.site.register(models.FooterLinkCategory)
admin.site.register(models.FooterLink, FooterLinkAdmin)
admin.site.register(models.Slider, SliderAdmin)
admin.site.register(models.SiteBanner, SiteBannerAdmin)
