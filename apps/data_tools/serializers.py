from drf_writable_nested import WritableNestedModelSerializer, UniqueFieldsMixin
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from .models import ThemeDirectory, DataSourceTable, DataSourceTableField, DirectoryTable


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    """支持动态指定字段的序列化器，传参fields，序列化和反序列化都支持"""
    Meta: type

    def __init__(self, *args, **kwargs):
        """支持字段动态生成的序列化器，从默认的Meta.fields中过滤，无关字段不查不序列化"""
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            allow = set(fields)
            existing = set(self.fields)
            for f in existing - allow:
                self.fields.pop(f)

    def __new__(cls, *args, **kwargs):
        """list序列化时，首先使用传参的fields，默认用meta.list_fields作为序列化字段"""
        if kwargs.pop('many', False):
            fields = getattr(cls.Meta, 'list_fields', None)
            if fields and 'fields' not in kwargs:
                kwargs['fields'] = fields
            return cls.many_init(*args, **kwargs)
        return super().__new__(cls, *args, **kwargs)


class DataSourceTableFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSourceTableField
        fields = ('column_name_cn', 'column_name_en', 'column_type', 'column_length', 'column_is_pk', 'is_list_show',
                  'ordinal_position', 'is_list_show', 'is_detail_show')


class DataSourceTableSerializer(WritableNestedModelSerializer):
    table_fields = DataSourceTableFieldSerializer(many=True)

    class Meta:
        model = DataSourceTable
        fields = (
            'table_data_source', 'table_name_zh', 'table_name_en', 'table_logical_name', 'table_fields')


class DirectoryTableSerializer(serializers.ModelSerializer):
    table_name = serializers.CharField(source='table_name_code.table_name_zh')
    table_source_type = serializers.CharField(source='table_name_code.table_data_source.data_source_type')
    table_source_url = serializers.CharField(source='table_name_code.table_data_source.data_source_url')
    table_source_extend = serializers.CharField(source='table_name_code.table_data_source.extend')

    class Meta:
        model = DirectoryTable
        fields = ('id', 'table_name_code', 'table_name', 'table_source_url', 'table_source_type', 'table_source_extend')


class ThemeDirectorySerializer(DynamicFieldsModelSerializer):
    direct_name_table = DirectoryTableSerializer(many=True, read_only=True)
    children = RecursiveField(required=False, allow_null=True, many=True)

    class Meta:
        model = ThemeDirectory
        fields = ("id", "name", 'parent', 'children', 'direct_name_table')
        list_fields = ('id', 'name', 'parent', 'children', 'level', 'direct_name_table')
