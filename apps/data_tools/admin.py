from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import DataSource, DataSourceType, DataSourceTable, DataSourceTableField, ThemeDirectory, DirectoryTable


class DataSourceTableFieldline(admin.TabularInline):
    # resource_class = DataSourceTableFieldForm
    model = DataSourceTableField
    list_display = (
        'column_name_cn', 'column_name_en', 'column_type', 'column_length', 'ordinal_position', 'column_is_pk')
    extra = 0


@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ['meta_source_type', 'data_source_name', 'user_name', 'db_name']
    search_fields = ['data_source_name']
    list_display_links = ['data_source_name']

    def meta_source_type(self, obj):
        return obj.data_source_type

    meta_source_type.short_description = "数据源类型"


@admin.register(DataSourceTable)
class DataSourceTableAdmin(admin.ModelAdmin):
    inlines = [DataSourceTableFieldline]
    list_display = ['table_name_zh', 'table_name_en', 'table_logical_name', 'table_code', 'tb_data_source',
                    'table_sort_id']
    search_fields = ['table_name_zh', 'table_name_en']
    list_display_links = ['table_name_en']

    def tb_data_source(self, obj):
        return obj.table_data_source

    tb_data_source.short_description = "数据源名称"

    class Media:
        css = {"all": ("css/hide_admin_original.css",)}


@admin.register(DataSourceTableField)
class DataSourceTableFieldAdmin(admin.ModelAdmin):
    list_display = [
        'ordinal_position', 'column_name_cn', 'column_name_en', 'column_type', 'column_length', 'column_is_pk']
    search_fields = ['column_name_cn', 'column_name_en']
    list_display_links = ['column_name_cn']


@admin.register(ThemeDirectory)
class ThemeDirectoryAdmin(MPTTModelAdmin):
    list_display = ('name',)
    mptt_level_indent = 20
    mptt_indent_field = "name"


@admin.register(DirectoryTable)
class DirectoryTableAdmin(admin.ModelAdmin):
    list_display = ('table_name_code', 'directory',)

    fieldsets = (
        (None, {'fields': ('table_name_code', 'direct_name')}),
    )

    def directory(self, obj):
        list_dir = []
        for btz in obj.direct_name.get_ancestors():
            list_dir.append(btz.name)
        list_dir.append(obj.direct_name.name)
        print(list_dir)
        return '/'.join(list_dir)

    directory.short_description = "关联目录"


admin.site.site_header = '元数据管理系统'
admin.site.index_title = '首页'
admin.site.register(DataSourceType)
# Register your models here.
