"""
Created on 2020年3月4日
应用apps
插件
api开发
@author: x1312
"""
from django.urls import re_path, path
from apps.extension_tools.views import sum_all, video
from django.views.decorators.cache import cache_page  # 缓存设置时间的意义在于，多长时间内的内容不变

app_name = 'extension_tools'
urlpatterns = [
    re_path(r'^sumall/', cache_page(60 * 15)(sum_all), name='sum_all'),
    re_path(r'^video/(?P<video_url>.+)/$', cache_page(60 * 15)(video), name='video'),
]
