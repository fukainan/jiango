# -*- coding: utf-8 -*-
# Created on 2015-10-13
# @author: Yefei
"""
from jiango.cms.urls import urlpatterns as cms_urls

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin_urls()),
    url(r'^api/captcha/', include('jiango.captcha.urls')),
    url(r'^api/', api_urls()),
    *cms_urls # root include
)
"""

from django.urls import path
from . import views

urlpatterns = [
    path('<path:path>/page.<int:page>/', views.content_list, name='cms-list'),
    path('<path:path>/<int:content_id>/', views.content_show, name='cms-content'),
    path('<path:path>/', views.column, name='cms-column'),
]
