# -*- coding: utf-8 -*-
# @Time    : 2022/12/28 15:58
# @Author  : DivingKitten
# @desc    :

from django.urls import re_path, path, include
from rest_framework.routers import DefaultRouter
from apps.users.views import UserProfileViewSits

router = DefaultRouter()
router.register(r'user', UserProfileViewSits, basename='users')
urlpatterns = [
    re_path(r'', include(router.urls)),
]
