# -*- coding: utf-8 -*-
# Created on 2015-9-2
# @author: Yefei
from .auth import get_request_user
from django.utils.deprecation import MiddlewareMixin


class AuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        get_request_user(request)
