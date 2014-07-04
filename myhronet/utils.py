# -*- coding: utf-8 -*-


def get_client_ip(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip:
        return ip.split(', ')[0]
    else:
        return request.META['REMOTE_ADDR']
