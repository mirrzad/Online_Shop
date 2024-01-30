from django import template
from jalali_date import datetime2jalali, date2jalali


register = template.Library()


@register.filter(name='show_jalali_date')
def show_jalali_date(date):
    return date2jalali(date)


@register.filter(name='show_jalali_time')
def show_jalali_time(date):
    return date.strftime('%H:%M')


@register.filter(name='three_digits')
def three_digits(value):
    return f"{value:,}"

