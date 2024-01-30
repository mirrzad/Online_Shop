from django.db import models


class SiteSettings(models.Model):
    site_title = models.CharField(max_length=200, verbose_name='نام سایت')
    site_url = models.CharField(max_length=200, verbose_name='دامنه سایت')
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name='آدرس')
    phone = models.CharField(max_length=200, null=True, blank=True, verbose_name='تلفن')
    fax = models.CharField(max_length=200, null=True, blank=True, verbose_name='فکس')
    email = models.CharField(max_length=200, null=True, blank=True, verbose_name='ایمیل')
    copy_right = models.TextField(verbose_name='متن کپی رایت')
    about_us = models.TextField(verbose_name='درباره ما')
    main_logo = models.ImageField(upload_to='images/site_settings', verbose_name='عکس لوگو')
    is_main_setting = models.BooleanField(verbose_name='تنظیمات اصلی')

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات'

    def __str__(self):
        return self.site_title


class FooterLinkCategory(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')

    class Meta:
        verbose_name = 'دسته بندی لینک های فوتر'
        verbose_name_plural = 'دسته بندی های لینک های فوتر'

    def __str__(self):
        return self.title


class FooterLink(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    url = models.URLField(max_length=200, verbose_name='آدرس')
    footer_link_category = models.ForeignKey(FooterLinkCategory, on_delete=models.CASCADE, verbose_name='دسته بندی')

    class Meta:
        verbose_name = ' لینک فوتر'
        verbose_name_plural = ' لینک های فوتر'

    def __str__(self):
        return self.title


class Slider(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    url = models.URLField(max_length=50, verbose_name='لینک')
    url_title = models.CharField(max_length=50, verbose_name='عنوان لینک')
    description = models.TextField(verbose_name='توضیحات اسلایدر')
    image = models.ImageField(upload_to='images/slider', verbose_name='عکس اسلایدر')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')

    class Meta:
        verbose_name = 'تنظیمات اسلایدر'
        verbose_name_plural = ' تنظیمات اسلایدرها'

    def __str__(self):
        return self.title


class SiteBanner(models.Model):
    class SiteBannerPosition(models.TextChoices):
        product_list = 'product_list', 'صفحه لیست محصولات'
        product_detail = 'product_detail', 'صفحه جزئیات محصولات'
        about_us = 'about_us', 'درباره ما'

    title = models.CharField(max_length=100, verbose_name='عنوان')
    url = models.URLField(max_length=400, null=True, blank=True, verbose_name='آدرس')
    is_active = models.BooleanField(verbose_name='فعال/غیرفعال')
    image = models.ImageField(upload_to='images/banner', verbose_name='عکس بنر')
    position = models.CharField(max_length=100, verbose_name='جایگاه نمایش', choices=SiteBannerPosition.choices)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'بنر تبلیغاتی'
        verbose_name_plural = 'بنرهای تبلیغاتی'