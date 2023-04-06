import os, uuid
from django.conf import settings
from django.db import models
from django.utils import timezone

from mdeditor.fields import MDTextField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill



def user_mugshot_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:8], ext)
    return os.path.join('login/uploads/avatar', str(instance.id), filename)


# 分类
class Category(models.Model):
    name = models.CharField(verbose_name='文章类别', max_length=20)

    class Meta:
        verbose_name = '文章类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 文章标签
class Tag(models.Model):
    name = models.CharField(verbose_name='文章标签', max_length=20)

    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 博客
class Blog(models.Model):
    name = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='标题', max_length=100)
    content = MDTextField(verbose_name='正文', config_name='my_config')
    create_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    update_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    views = models.IntegerField(verbose_name='阅读量', default=0)
    category = models.ForeignKey(Category, verbose_name='文章类别', related_name='cate_blog', on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField(Tag, verbose_name='文章标签', )  # 多对多的外键关系
    # img = ProcessedImageField(verbose_name="封面图片", upload_to=user_mugshot_path,
    #                           processors=[ResizeToFill(45, 45)],
    #                           format='JPEG',
    #                           options={'quality': 95})

    class Meta:
        verbose_name = '我的博客'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']

    def increase_views(self):  # 增加模型方法
        self.views += 1
        self.save(update_fields=['views', ])

    def tags_list(self):  # 后台显示标签
        return ','.join([tag.name for tag in self.tags.all()])

    def __str__(self):
        return self.title


# 推荐位
class Tui(models.Model):
    name = models.CharField('推荐位', max_length=100)

    class Meta:
        verbose_name = '推荐位'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 轮播图
class Banner(models.Model):
    text_info = models.CharField('标题', max_length=50, default='')
    img = ProcessedImageField(verbose_name="轮播图", upload_to=user_mugshot_path,
                              processors=[ResizeToFill(45, 45)],
                              format='JPEG',
                              options={'quality': 95})

    link_url = models.URLField('图片链接', max_length=1000)
    is_active = models.BooleanField('是否是active', default=False)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = '轮播图'

    def __str__(self):
        return self.text_info
