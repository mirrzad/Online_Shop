from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from account_module.models import User


class ProductCategory(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان', db_index=True)
    url_title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان url')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class ProductBrand(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name='نام برند')
    url_title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان url')
    is_active = models.BooleanField(verbose_name=' فعال/ غیر فعال')

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند ها'

    def __str__(self):
        return self.title


class Product(models.Model):
    category = models.ManyToManyField(
        ProductCategory, related_name='products', verbose_name='دسته بندی ها'
    )
    title = models.CharField(max_length=300, verbose_name='عنوان', db_index=True)
    price = models.IntegerField(null=True, verbose_name='قیمت')
    short_description = models.CharField(
        max_length=400, null=True, blank=True,
        verbose_name='توضیحات کوتاه', db_index=True
    )
    image = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='عکس محصول')
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, null=True, blank=True, verbose_name='برند')
    description = models.TextField(verbose_name='توضیحات اصلی')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')
    slug = models.SlugField(default='', null=False, db_index=True, unique=True, max_length=200)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class ProductTag(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name='عنوان تگ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_tags')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'تگ محصول'
        verbose_name_plural = 'تگ های محصولات'


class ProductVisit(models.Model):
    product = models.ForeignKey(
        'Product', on_delete=models.CASCADE, verbose_name='بازدید محصول', related_name='visits')
    ip = models.CharField(max_length=50, verbose_name='آی پی کاربر')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', null=True, blank=True)

    def __str__(self):
        return f'{self.product.title} / {self.ip}'

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدید محصولات'


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول', related_name='galleries')
    image = models.ImageField(upload_to='images/product_gallery')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'گالری محصول'
        verbose_name_plural = 'گالری محصولات'

