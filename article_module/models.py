from django.db import models
from jalali_date import datetime2jalali, date2jalali
from account_module.models import User


class ArticleCategory(models.Model):
    parent = models.ForeignKey('ArticleCategory', on_delete=models.CASCADE,
                               null=True, blank=True, verbose_name='دسته بندی والد')
    title = models.CharField(max_length=200, verbose_name='عنوان')
    url_title = models.CharField(max_length=200, verbose_name='عنوان در url')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')

    class Meta:
        verbose_name = 'دسته بندی مقالات'
        verbose_name_plural = 'دسته بندی های مقالات'

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    slug = models.SlugField(max_length=500, db_index=True, allow_unicode=True, verbose_name='عنوان در url')
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    body = models.TextField(verbose_name='متن مقاله')
    image = models.ImageField(upload_to='images/articles', verbose_name='عکس مقاله')
    date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ انتشار')
    categories = models.ManyToManyField(ArticleCategory, verbose_name='دسته بندی ها')
    is_active = models.BooleanField(default=True, verbose_name='فعال/غیرفعال')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده', editable=False, null=True)

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def __str__(self):
        return self.title

    def get_jalali_date(self):
        return datetime2jalali(self.date)

    def get_jalali_time(self):
        return self.date.strftime('%H:%M')


class ArticleComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='مطلب')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    parent = models.ForeignKey('ArticleComment', on_delete=models.CASCADE,
                               verbose_name='نظر والد', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    text = models.TextField(verbose_name='متن نظر')

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت های مقالات'

    def __str__(self):
        return str(self.user)
