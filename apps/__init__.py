# -*- coding: utf-8 -*-
# @Time    : 2022/12/28 11:42
# @Author  : DivingKitten
# @desc    :
from django.contrib import admin
from django.contrib.admin.apps import AdminConfig

apps_order_list = ['users', 'auth', 'blogs', 'data_tools', 'extension_tools']
apps_order_dict = {app: index for index, app in enumerate(apps_order_list)}


class XAdminSite(admin.AdminSite):

    def index(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}

        app_list = self.get_app_list(request)
        app_dict = self._build_app_dict(request)

        print(app_dict.keys())

        app_list.sort(key=lambda element_dict: apps_order_dict[element_dict["app_label"]])

        extra_context['app_list'] = app_list
        return super(XAdminSite, self).index(request, extra_context)


class XAdminConfig(AdminConfig):
    default_site = 'apps.XAdminSite'
