# -*- coding: utf-8 -*-
# Created on 2015-9-1
# @author: Yefei
from inspect import isfunction
from django.urls import path, include
from django.utils.text import capfirst
from collections import OrderedDict
from django.urls import reverse, resolve
from jiango.importlib import autodiscover_installed_apps
from . import views

# A flag to tell us if autodiscover is running.  autodiscover will set this to
# True while running, and False when it finishes.
LOADING = False
loaded_modules = OrderedDict()


def autodiscover(module_name):
    global LOADING
    if LOADING:
        return
    LOADING = True
    for namesapce, module in autodiscover_installed_apps(module_name):
        if hasattr(module, 'urlpatterns'):
            loaded_modules[module] = namesapce
    # autodiscover was successful, reset loading flag.
    LOADING = False


urlpatterns = [
    path('', views.index, name='-index'),
    path('-/login', views.login, name='-login'),
    path('-/logout', views.logout, name='-logout'),
    path('-/password', views.set_password, name='-password'),

    path('-/log', views.log_list, name='-log'),
    path('-/log/<int:log_id>', views.log_show, name='-log-show'),

    path('-/user', views.user_list, name='-user'),
    path('-/user/add', views.user_edit, name='-user-add'),
    path('-/user/<int:user_id>', views.user_show, name='-user-show'),
    path('-/user/<int:user_id>/edit', views.user_edit, name='-user-edit'),
    path('-/user/<int:user_id>/password', views.set_password, name='-user-password'),
    path('-/user/<int:user_id>/delete', views.user_delete, name='-user-delete'),

    path('-/group', views.group_list, name='-group'),
    path('-/group/add', views.group_edit, name='-group-add'),
    path('-/group/<int:group_id>', views.group_show, name='-group-show'),
    path('-/group/<int:group_id>/edit', views.group_edit, name='-group-edit'),
    path('-/group/<int:group_id>/delete', views.group_delete, name='-group-delete'),
]

system_sub_menus = [
    # url_name, name, icon
    ('admin:-index', u'系统首页', 'fa fa-dashboard'),
    ('admin:-log', u'系统日志', 'fa fa-file-text-o'),
    ('admin:-user', u'管理员', 'fa fa-user'),
    ('admin:-group', u'管理组', 'fa fa-group'),
    ('admin:-password', u'修改密码', 'fa fa-lock'),
]


def _get_sub_menus(current_view_name, sub_menus):
    return [dict(url=reverse(_url),
                 verbose_name=_name,
                 icon=_icon,
                 is_active=current_view_name.startswith(_url)) for _url, _name, _icon in sub_menus]


def get_navigation(request):
    navigation = []
    current_view_name = resolve(request.path).view_name
    for module, app_name in loaded_modules.items():
        icon = getattr(module, 'icon', None)
        icon = icon(request) if isfunction(icon) else icon

        verbose_name = getattr(module, 'verbose_name', capfirst(app_name))
        verbose_name = verbose_name(request) if isfunction(verbose_name) else verbose_name
        if not verbose_name:
            continue

        sub_menus = getattr(module, 'sub_menus', [])
        sub_menus = sub_menus(request) if isfunction(sub_menus) else sub_menus
        sub_menus = _get_sub_menus(current_view_name, sub_menus)

        is_active = current_view_name.startswith('admin:%s' % app_name)

        navigation.append(dict(url=reverse('admin:%s:index' % app_name),
                               verbose_name=verbose_name,
                               icon=icon,
                               sub_menus=sub_menus,
                               is_active=is_active))

    navigation.append(dict(url=reverse('admin:-index'),
                           verbose_name=u'系统',
                           icon=None,
                           sub_menus=_get_sub_menus(current_view_name, system_sub_menus),
                           is_active=current_view_name.startswith('admin:-')))
    return navigation


def get_app_verbose_name(app_name):
    for module, _app_name in loaded_modules.items():
        if app_name == _app_name:
            verbose_name = getattr(module, 'verbose_name', capfirst(app_name))
            if isfunction(verbose_name):
                verbose_name = verbose_name(None)
            return verbose_name
    return capfirst(app_name)


def admin_urls(module_name='admin'):
    autodiscover(module_name)
    for module, app_name in loaded_modules.items():
        urlpatterns.append(path('%s' % app_name, include((module.urlpatterns, app_name))))
    return include((urlpatterns, 'admin'))
