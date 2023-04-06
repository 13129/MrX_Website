from rest_framework import serializers
from apps.users.models import Users


class UserProfileSerializer(serializers.ModelSerializer):
    """用户详细信息序列化器"""

    class Meta:
        model = Users
        fields = ('id', 'username', 'nickname', 'email', 'date_joined',
                  'register_ip', 'last_login_ip', 'is_superuser', 'is_staff',)

        read_only_fields = ('id', 'username', 'date_joined',
                            'register_ip', 'last_login_ip', 'is_superuser', 'is_staff',)
