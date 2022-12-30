from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin  # 从django继承过来定制
from django.contrib.auth.forms import ReadOnlyPasswordHashField  # 哈希加密
from django.db.models import Q
from django.utils.translation import gettext_lazy as _  # 字段国际化

from .models import Users
from django.contrib.auth.models import Group

class UserCreationForm(forms.ModelForm):
    """创建新用户的表单"""
    username = forms.CharField(label='用户名', widget=forms.TextInput)
    password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput)

    class Meta:
        model = Users
        fields = ['username', 'password1', 'password2', 'email']

    def clean_password2(self):
        # 检查密码是否匹配
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("密码不匹配")
        return password2

    def save(self, commit=True):
        # 密码哈希加密
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """用于修改用户的表单。将密码字段替换为管理员的密码加密显示字段。"""
    password = ReadOnlyPasswordHashField()  # hash加密

    class Meta:
        model = Users
        fields = ['username', 'password', 'email']

    def clean_password(self):
        # 无论用户提供什么，都返回初始值,字段无权访问初始值
        return self.initial["password"]


@admin.register(Users)
class UsersAdmin(BaseUserAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_display = ('image_data', 'username', 'email', 'is_active', 'is_staff',)
        self.search_fields = ('username', 'email',)
        self.list_display_links = ('username',)
        self.list_filter = ('last_login',)
        self.form = UserChangeForm  # 编辑用户表单，使用自定义的表单
        self.add_form = UserCreationForm

    # 重写用户权限
    def changelist_view(self, request, extra_context=None):
        # 这个方法在源码的admin/options.py文件的ModelAdmin这个类中定义，不同权限的用户，返回的表单内容不同
        if not request.user.is_superuser:  # 用于显示用户模型的字段。这些将覆盖基本UserAdmin上的定义,引用auth.User上的特定字段。
            self.fieldsets = ((None,
                               {'fields': ('mugshot', 'username', 'password',)}),
                              (_('Personal info'), {'fields': ('email',)}),
                              # _ 将('')里的内容国际化,这样可以让admin里的文字自动随着LANGUAGE_CODE切换中英文
                              (_('Permissions'), {'fields': ('is_active', 'is_staff', 'groups')}),
                              )
            # 这里('Permissions')中没有'is_superuser',此字段定义UserChangeForm表单中的具体显示内容，并可以分类显示
            self.add_fieldsets = ((None, {'classes': ('wide',),
                                          'fields': (
                                              'mugshot', 'username', 'password1', 'password2', 'email', 'is_active',
                                              'groups'),
                                          }),
                                  )
        else:  # super账户可以做任何事
            self.fieldsets = ((None, {'fields': ('mugshot', 'username', 'password',)}),
                              (_('Personal info'), {'fields': ('email',)}),
                              (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
                              )
            self.add_fieldsets = ((None, {'classes': ('wide',),
                                          'fields': (
                                              'mugshot', 'username', 'password1', 'password2', 'email', 'is_active',
                                              'is_staff', 'is_superuser', 'groups'),
                                          }),
                                  )
        return super().changelist_view(request, extra_context)

    def get_queryset(self, request):
        us = super().get_queryset(request)
        if request.user.is_superuser:
            return us
        else:
            current_group_set = Group.objects.get(user=request.user)
            group = Group.objects.get(name=current_group_set)
            users = group.user_set.filter(Q(username=request.user) | Q(is_staff=False,))
            return us.filter(Q(username=request.user) | Q())

# class UsersAdmin(admin.ModelAdmin):
#     list_display = ('image_data', 'username', 'email', 'is_active', 'is_staff', 'is_superuser')
#     search_fields = ('username', 'email',)
#     list_filter = ('last_login',)
#     list_display_links = ('username',)
#     # readonly_fields = ('image_data',)
#     form = UserChangeForm  # 编辑用户表单，使用自定义的表单
#     add_form = UserCreationForm
#
#     fieldsets = ((None, {'fields': ('mugshot', 'nickname', 'password',)}),
#                  (_('Personal info'), {'fields': ('email',)}),
#                  (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
#                  )
#     add_fieldsets = ((None, {'classes': ('wide',),
#                              'fields': (
#                                  'mugshot', 'nickname', 'username', 'password1', 'password2', 'email',
#                                  'is_active',
#                                  'is_staff', 'is_superuser', 'groups'),
#                              }),
#                      )
