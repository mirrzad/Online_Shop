from django.db import models

from account_module.models import User
from product_module.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر', related_name='orders')
    is_paid = models.BooleanField(verbose_name='نهایی شده/نشده')
    payment_date = models.DateTimeField(null=True, blank=True, verbose_name='تاریخ پرداخت')

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد های خرید کاربران'

    def calculate_total_amount(self):
        if self.is_paid:
            total_amount = 0
            for order_detail in self.orderdetails.all():
                total_amount += order_detail.final_price * order_detail.count
        else:
            total_amount = 0
            for order_detail in self.orderdetails.all():
                total_amount += order_detail.product.price * order_detail.count
        return total_amount


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید', related_name='orderdetails')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول', related_name='productorders')
    final_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت تمام شده')
    count = models.SmallIntegerField(verbose_name='تعداد')

    class Meta:
        verbose_name = 'جزئیات سبد خرید'
        verbose_name_plural = 'لیست جزئیات سبد خرید'

    def __str__(self):
        return str(self.order)

    def get_total_price(self):
        return self.product.price * self.count
