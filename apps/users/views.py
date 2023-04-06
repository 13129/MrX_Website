from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

from apps.users.serializers import UserProfileSerializer
from apps.users.models import Users


class UserProfileViewSits(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """查询/更新/一个对象,使用GenericAPIView时需绑定---get,post方法,只有登录用户有权限更新参数"""
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        # print(Users.objects.filter(username=self.request.user))
        return Users.objects.filter(username=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), ]
        return super().get_permissions()
