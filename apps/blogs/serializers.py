from rest_framework import serializers

from apps.blogs.models import Blog, Tag, Category, Banner


class TagSerializer(serializers.ModelSerializer):
    """博客标签序列化"""
    num = serializers.ReadOnlyField()

    class Meta:
        model = Tag
        fields = ('id', 'name', 'num')


class BlogSerializer(serializers.ModelSerializer):
    """博客信息序列化"""
    url = serializers.HyperlinkedIdentityField(view_name='blogs:blogs-detail')
    name = serializers.CharField(source='name.nickname', read_only=True)
    tags = serializers.CharField(source='tags_list', read_only=True)
    category = serializers.CharField(source='category.name', read_only=True)

    # category = serializers.SerializerMethodField('get_category')
    # name = serializers.SerializerMethodField('get_name')
    # tagss =  TagSerializer(many=True, read_only=True)
    class Meta:
        model = Blog
        fields = ('id', 'name', 'title', 'content', 'create_time', 'update_time', 'views', 'category', 'tags')
        read_only_fields = ('id', 'name', 'title', 'content', 'create_time', 'update_time', 'views', 'category', 'tags')

    # 动态修改字段
    def __init__(self, *args, **kwargs):
        remove_fields = kwargs.pop('remove_fields', None)
        super(BlogSerializer, self).__init__(*args, **kwargs)
        if remove_fields:
            for field_name in remove_fields:
                self.fields.pop(field_name)
    # def get_category(self,obj):
    #     return obj.category.name
    # def get_name(self,obj):
    #     return obj.name.username


class CategorySerializer(serializers.ModelSerializer):
    """博客标签序列化"""
    cate_blog = serializers.SerializerMethodField()

    # url = serializers.HyperlinkedIdentityField(view_name = 'blog:category-detail')
    # blog = BlogSerializer()
    # blog_set = serializers.StringRelatedField(many = True)
    # blog_set = serializers.SlugRelatedField(read_only = True, slug_field ='')
    @staticmethod
    def get_cate_blog(obj):
        blog = Blog.objects.filter(category=obj.id)

        if blog is not None and len(blog) > 0:
            return BlogSerializer(blog, many=True, remove_fields=['update_time', 'content', ]).data
        else:
            return ''

    class Meta:
        model = Category
        fields = ('id', 'name', 'cate_blog',)
        # model = Category
        # fields = ("url","id","name","blog_set")
        # depth = 1


class CategorySimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ("id", "text_info", "link_url", "is_active")
