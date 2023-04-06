from rest_framework import viewsets, mixins
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.blogs.models import Category, Blog, Banner, Tag
from apps.blogs.serializers import CategorySerializer, TagSerializer, BlogSerializer, BannerSerializer, \
    CategorySimpleSerializer


class BlogViewSit(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """查询一个和多个.list(),.retrieve()],重写retrieve()方法,实现文章访问量增加"""

    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increase_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CategoryViewSit(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySimpleSerializer
        else:
            return CategorySerializer


# 分类视图
class CategoryView(APIView):
    def get(self, request, pk):
        queryset = Category.objects.filter(id=pk)
        cate_serializer = CategorySerializer(queryset, many=True, context={'request': request})
        return Response({"cate": cate_serializer.data})


# 标签视图
class TagView(APIView):
    def get(self, request):
        queryset = Tag.objects.raw("""select bt.id,count(bt.id) as num ,bt.name from blog_blog ur
										left join blog_blog_tagss bbt on ur.id=bbt.blog_id
										left join blog_tag bt on bbt.tag_id = bt.id
										group by bt.id,bt.name
										order by name;""")

        tag_serializer = TagSerializer(queryset, many=True)
        return Response({"tag": tag_serializer.data})


# 自定义加密翻页
class MyLimitOffsetPagination(CursorPagination):
    cursor_query_param = 'cursor'
    page_size = 10
    ordering = 'id'
    page_size_query_param = 'size'
    max_page_size = 10


# 主页视图
class IndexView(APIView):
    def get(self, request):
        cate = Category.objects.all()
        tag = Tag.objects.all()
        blog = Blog.objects.all()
        # blog = Blog.objects.filter(~Q(category= '1'))
        banner = Banner.objects.all().filter(is_active=True)

        cate_serializer = CategorySerializer(cate, many=True, context={'request': request})
        tag_serializer = TagSerializer(tag, many=True)
        banner_serializer = BannerSerializer(banner, many=True)

        pg = MyLimitOffsetPagination()
        pager_blog = pg.paginate_queryset(queryset=blog, request=request, view=self)
        blog_serializer = BlogSerializer(pager_blog, many=True, context={'request': request})
        print("测试数据", blog_serializer.data)
        # 在数据库中获取分页数据
        return pg.get_paginated_response({
            'cate': cate_serializer.data,
            'tag': tag_serializer.data,
            'banner': banner_serializer.data,
            'blog': blog_serializer.data,
        })


class BlogView(APIView):
    def get(self, request, pk):
        blog = Blog.objects.filter(id=pk)
        blog_serializer = BlogSerializer(blog, many=True, context={'request': request})
        return Response({"blog": blog_serializer.data})
