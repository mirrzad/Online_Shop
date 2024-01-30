import time

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpRequest
from django.shortcuts import render, redirect
import requests
import json

from django.urls import reverse

from order_module.models import Order, OrderDetail
from product_module.models import Product


MERCHANT = 'test'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 11000  # Rial / Required
description = "نهایی کردن خرید شما از سایت ما"  # Required
email = ''  # Optional
mobile = ''  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:8000/order/verify-payment/'


def add_to_order(request):
    product_id = int(request.GET.get('product_id'))
    count = int(request.GET.get('count'))
    if count < 1:
        return JsonResponse({
            'status': 'invalid_input',
            'title': 'اعلان',
            'text': 'تعداد محصول وارد شده معتبر نمی باشد.',
            'icon': 'error',
            'confirmButtonText': 'ورود مجدد'
        })

    if request.user.is_authenticated:
        product = Product.objects.filter(is_active=True, is_delete=False, id=product_id).first()
        if product is not None:
            current_order, create = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
            current_order_detail = current_order.orderdetails.filter(product_id=product_id).first()
            if current_order_detail is not None:
                current_order_detail.count += count
                current_order_detail.save()
                return JsonResponse({
                    'status': 'success',
                    'title': 'اعلان',
                    'text': 'محصول مورد نظر با موفقیت به سبد خرید اضافه شد.',
                    'icon': 'success',
                    'confirmButtonText': 'تایید'
                })
            else:
                new_order = OrderDetail(order_id=current_order.id, product_id=product_id, count=count)
                new_order.save()
                return JsonResponse({
                    'status': 'success',
                    'title': 'اعلان',
                    'text': 'محصول مورد نظر با موفقیت به سبد خرید اضافه شد.',
                    'icon': 'success',
                    'confirmButtonText': 'تایید'
                })
        else:
            return JsonResponse({
                'status': 'not_found',
                'title': 'اعلان',
                'text': 'محصول مورد نظر یافت نشد.',
                'icon': 'error',
                'confirmButtonText': 'تلاش مجدد'
            })
    else:
        return JsonResponse({
            'status': 'not_authenticate',
            'title': 'اعلان',
            'text': 'ابتدا لاگین کنید.',
            'icon': 'error',
            'confirmButtonText': 'ورود به سایت'
        })


@login_required
def request_payment(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_amount()
    if total_price == 0:
        return redirect(reverse('user_basket_page'))

    req_data = {
        "merchant_id": MERCHANT,
        "amount": total_price * 10,
        "callback_url": CallbackURL,
        "description": description,
        # "metadata": {"mobile": mobile, "email": email}
    }
    req_header = {"accept": "application/json", "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


@login_required
def verify_payment(request: HttpRequest):
    current_order, created = Order.objects.prefetch_related('orderdetails').get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total_amount()
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        req_header = {"accept": "application/json", "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": total_price * 10,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                current_order.is_paid = True
                current_order.payment_date = time.time()
                for item in current_order.orderdetails.all():
                    item.final_price = item.product.price
                current_order.save()
                ref_str = str(req.json()['data']['ref_id'])
                return render(request, 'order_module/payment_result.html', {
                    'success': f'تراکنش شما با کد پیگیری {ref_str} با موفقیت انجام شد'
                })
            elif t_status == 101:
                return render(request, 'order_module/payment_result.html', {
                    'info': 'این تراکنش قبلا ثبت شده است'
                })
            else:
                # return HttpResponse('Transaction failed.\nStatus: ' + str(
                #     req.json()['data']['message']
                # ))
                return render(request, 'order_module/payment_result.html', {
                    'error': str(req.json()['data']['message'])
                })
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return render(request, 'order_module/payment_result.html', {
                'error': e_message
            })
    else:
        return render(request, 'order_module/payment_result.html', {
            'error': 'پرداخت با خطا مواجه شد / کاربر از پرداخت ممانعت کرد'
        })
