"""MrX_Website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from MrX_Website import settings

urlpatterns = [
    re_path(r'^media/(?P<path>.+)$', serve, {'document_root': settings.MEDIA_ROOT}),
    path('admin/', admin.site.urls),
    re_path(r'^api_auth/', include('rest_framework.urls', namespace='rest_framework')),
    re_path(r'mdeditor/', include('mdeditor.urls')),
    re_path(r'^api/blogs/', include('apps.blogs.urls')),
    re_path(r'^api/users/', include('apps.users.urls')),
    re_path(r'^api/extension_tools/', include('apps.extension_tools.urls', namespace='extension_tools')),
    re_path(r'^api/data_tools/', include('apps.data_tools.urls', namespace='data_tools')),

]
