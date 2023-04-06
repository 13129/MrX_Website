from django.contrib import admin

from apps.blogs.models import Category, Tag, Blog


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'create_time', 'update_time', 'views', 'category', 'tags_list')
    list_editable = ('title',)
    search_fields = ('title', 'name')
    list_filter = ('create_time', 'category',)
