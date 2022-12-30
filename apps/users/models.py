import uuid, os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.signals import user_logged_in
from django.utils.html import format_html

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# Create your models here.
def user_mugshot_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex[:8], ext)
    return os.path.join('login/uploads/avatar', str(instance.id), filename)


def get_ip_from_request(request):
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        user_ip = request.META.get("HTTP_X_FORWARDED_FOR")
    else:
        user_ip = request.META.get("HTTP_X_REAL_IP")
    print(user_ip)
    return user_ip


def update_last_login_ip(sender, user, request, **kwargs):
    """更新最后一次登录的地址"""
    ip = get_ip_from_request(request)
    if ip:
        user.last_login_ip = ip
        user.save()


user_logged_in.connect(update_last_login_ip)


class Users(AbstractUser):
    """
    用户模型自定义
    """
    last_login_ip = models.GenericIPAddressField("最近一次登录", unpack_ipv4=True, blank=True, null=True)
    register_ip = models.GenericIPAddressField("注册IP", unpack_ipv4=True, blank=True, null=True)
    nickname = models.CharField("昵称", max_length=50, unique=True)  # unique保持唯一性
    mugshot = ProcessedImageField(verbose_name="头像", upload_to=user_mugshot_path,
                                  processors=[ResizeToFill(45, 45)],
                                  format='JPEG',
                                  options={'quality': 95})

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username

    def image_data(self):
        if self.mugshot:
            return format_html('<img src="/media/{}" width="45px" height="45px"/>', self.mugshot)
        else:
            return format_html('<img src="/media/无拍照上传.png" width="45px" height="45px"/>')

    image_data.short_description = '头像'

    # def