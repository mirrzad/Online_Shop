from django.db import models


class ContactUs(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان')
    email = models.EmailField(max_length=300, verbose_name='ایمیل')
    full_name = models.CharField(max_length=300, verbose_name='نام و نام خانوادگی')
    message = models.TextField(verbose_name='متن پیام')
    response = models.TextField(verbose_name='متن پاسخ', null=True, blank=True)
    is_read_by_admin = models.BooleanField(verbose_name='خوانده شده توسط ادمین', default=False)
    created_date = models.DateTimeField(verbose_name='تاریخ ثبت', auto_now_add=True)

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'لیست تماس با ما'

    def __str__(self):
        return self.title


class ProfileImage(models.Model):
    profile_image = models.ImageField(upload_to='images', null=True, verbose_name='عکس کاربری')
