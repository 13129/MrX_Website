from apps.blogs import views
from rest_framework.routers import DefaultRouter
from django.urls import re_path, include

router = DefaultRouter()
router.register(r'blog', views.BlogViewSit, basename='blog')
router.register(r'category', views.CategoryViewSit, basename='category')


urlpatterns = [
    re_path(r'^', include(router.urls)),
    # re_path(r'index/$', IndexView.as_view()),
    # re_path(r'tag/$', views.TagView.as_view()),
    # re_path(r'category/(?P<pk>\d+)/$', views.CategoryView.as_view(), name='category-detail'),
    # re_path(r'blog/(?P<pk>\d+)/$', views.BlogView.as_view(), name='blog-detail'),
]
