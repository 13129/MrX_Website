import os
from django.db import models
from django.utils import timezone
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
import uuid


def video_upload_to(instance, filename):
    return 'video/{uuid}/{filename}'.format(uuid=uuid.uuid4().hex, filename=filename)


def user_mugshot_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:8], ext)
    return os.path.join('login/uploads/avatar', str(instance.id), filename)


class VideoCate(models.Model):
    name = models.CharField(u'视频类别', max_length=100, default='视频', null=False)

    class Meta:
        verbose_name = '视频分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class VideoUpload(models.Model):
    file = models.FileField(u'视频', upload_to=video_upload_to, null=False, blank=False)
    file_name = models.CharField(u'视频名称', max_length=100, default='默认时评', null=False)
    file_cate = models.ForeignKey(VideoCate, verbose_name='视频分类', on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(u'上传时间', default=timezone.now, null=False)
    comment = models.CharField(u'备注说明', max_length=100, null=False)

    class Meta:
        verbose_name = '视频上传'
        verbose_name_plural = verbose_name

    def __str__(self):  # 后台管理注册显示的类别名称
        return self.file_name

    def screenshots_as_list(self):
        sfd = str(self.file)
        return sfd.split('/')[2:]


# 详细访问信息
class Tourist(models.Model):
    IP = models.CharField(verbose_name='ip', max_length=30, default='...')
    location = models.CharField(verbose_name='ip所在地', max_length=30, default='')
    start_time = models.DateTimeField(verbose_name='请求时间', default=timezone.now)
    is_lock = models.BooleanField(verbose_name="访问状态", default=True)  # 锁定为1
    count = models.IntegerField(verbose_name='访问次数', default=0)

    class Meta:
        verbose_name = '访客信息'
        verbose_name_plural = verbose_name

    def __str__(self):  # 后台管理注册显示的类别名称
        return self.IP


# 友链接
class Link(models.Model):
    name = models.CharField(verbose_name='链接名字', max_length=20)
    link_url = models.URLField(verbose_name='链接网址', max_length=100)
    link_img = ProcessedImageField(verbose_name="封面图片", upload_to=user_mugshot_path,
                                   processors=[ResizeToFill(45, 45)],
                                   format='JPEG',
                                   options={'quality': 95})
    add_time = models.DateTimeField(verbose_name='添加时间', default=timezone.now)
    mod_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)

    class Meta:
        verbose_name = '友链接'
        verbose_name_plural = verbose_name

    def __str__(self):  # 后台管理注册显示的类别名称
        return self.name


# 公告栏
notice_types = (('sticky', '置顶'), ('latest', '最新'), ('ordinary', '一般'))


class Notice(models.Model):
    detail = models.TextField(verbose_name="公告内容")
    level = models.CharField(max_length=30, choices=notice_types, default='最新')
    release_time = models.DateTimeField(verbose_name="发布时间", default=timezone.now)
    mod_time = models.DateTimeField(verbose_name="时间", auto_now=True)

    class Meta:
        verbose_name = '网站公告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.detail
