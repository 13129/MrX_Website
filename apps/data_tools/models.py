import uuid
from mptt.models import MPTTModel, TreeForeignKey

from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class DataSourceType(models.Model):
    data_source_type_name = models.CharField(max_length=255, unique=True, verbose_name="数据源类型")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.data_source_type_name

    class Meta:
        verbose_name = '数据源类型'
        verbose_name_plural = "数据源类型"
        ordering = ['-create_time']


class DataSource(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="数据源id")
    data_source_name = models.CharField(max_length=255, unique=True, verbose_name="数据源名称")
    data_source_type = models.ForeignKey(DataSourceType, on_delete=models.CASCADE, to_field='data_source_type_name')
    ip_address = models.GenericIPAddressField(max_length=128, verbose_name="ip地址")
    port = models.PositiveSmallIntegerField(verbose_name="端口")
    user_name = models.CharField(max_length=128, verbose_name="用户名", null=True, blank=True)
    pass_word = models.CharField(max_length=128, verbose_name="密码", null=True, blank=True)
    db_name = models.CharField(max_length=128, verbose_name="数据库名称", null=True, blank=True)
    data_source_url = models.CharField(max_length=500, verbose_name="数据源链接")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    extend = models.JSONField(verbose_name="扩展属性", null=True, blank=True)

    def __str__(self):
        return self.data_source_name

    class Meta:
        verbose_name = '数据源管理'
        verbose_name_plural = "数据源管理"
        ordering = ['-update_time']


class DataSourceTable(models.Model):
    table_code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='表编码')
    table_data_source = models.ForeignKey(DataSource, on_delete=models.CASCADE, verbose_name='数据源名称')
    table_name_zh = models.CharField(max_length=255, verbose_name="表显示名", null=True, blank=True)
    table_name_en = models.CharField(max_length=255, verbose_name="表物理名")
    table_logical_name = models.CharField(max_length=255, verbose_name="逻辑表名", null=True, blank=True)
    table_sort_id = models.PositiveSmallIntegerField(verbose_name="排序", default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.table_name_en

    class Meta:
        verbose_name = '表管理'
        verbose_name_plural = "表管理"
        ordering = ['table_sort_id', '-update_time']


class ColumnTypeChoices(models.TextChoices):
    CHAR = 'char', _('char')
    VARCHAR = 'varchar', _('varchar')
    INT = 'int', _('int')
    TEXT = 'text', _('text')
    DATE = 'date', _('date')
    TIMESTAMP = 'timestamp', _('timestamp')
    FLOAT = 'float', _('float')
    BOOL = 'bool', _('bool')
    JSONB = 'jsonb', _('jsonb')


class DataSourceTableField(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    column_name_cn = models.CharField(max_length=64, verbose_name="字段显示名", null=True, blank=True)
    column_name_en = models.CharField(max_length=64, verbose_name="字段物理名")
    column_type = models.CharField(max_length=32, verbose_name="字段类型", choices=ColumnTypeChoices.choices,
                                   default=ColumnTypeChoices.VARCHAR, )
    table_code = models.ForeignKey(DataSourceTable, on_delete=models.CASCADE,
                                   verbose_name='表物理名', related_name='table_fields')
    column_length = models.CharField(max_length=32, verbose_name="字段长度")
    ordinal_position = models.PositiveSmallIntegerField(verbose_name="排序", default=0)
    column_is_pk = models.BooleanField(verbose_name="主键", default=False)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    is_list_show = models.BooleanField(verbose_name="列表显示", default=False)
    is_detail_show = models.BooleanField(verbose_name="详情显示", default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = '字段管理'
        verbose_name_plural = "字段管理"
        # unique_together = ('column_name_en', 'tb_field_code',)
        ordering = ['ordinal_position', 'create_time']


class ThemeDirectory(MPTTModel):
    name = models.CharField('目录名称', max_length=50, unique=True)
    parent = TreeForeignKey('self', verbose_name='上级目录', on_delete=models.CASCADE, null=True, blank=True,
                            related_name='children')

    class Meta:
        verbose_name = verbose_name_plural = '目录管理'

    def __str__(self):
        return self.name


class DirectoryTable(models.Model):
    table_name_code = models.OneToOneField("DataSourceTable", on_delete=models.CASCADE,
                                           verbose_name='表名称', blank=True, null=True)
    direct_name = models.ForeignKey(ThemeDirectory, on_delete=models.CASCADE, verbose_name='目录', blank=True, null=True,
                                    related_name='direct_name_table')

    def __str__(self):
        if self.table_name_code.table_name_zh:
            return self.table_name_code.table_name_zh
        else:
            return '-'

    class Meta:
        verbose_name = verbose_name_plural = '目录关联管理'
