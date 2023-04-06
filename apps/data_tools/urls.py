from django.urls import re_path

from .views import DirectoryAPIView, TableDataAPIView, DataSourceTablesView

app_name = 'polls'
urlpatterns = [
    re_path(r'^catalog/$', DirectoryAPIView.as_view()),
    re_path(r'^catalog/table/fields/list/$', DirectoryAPIView.as_view()),
    re_path(r'^catalog/table/create/$', DataSourceTablesView.as_view()),
    # re_path(r'^catalog/table/info/search/$', DirectoryAPIView.as_view()),
    re_path(r'^catalog/table/data/search/$', TableDataAPIView.as_view()),
]