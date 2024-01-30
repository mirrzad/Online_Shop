from django.http import HttpRequest


def get_client_ip(request: HttpRequest):
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip = request.META.get('HTTP_X_FORWARDED_FOR').split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
