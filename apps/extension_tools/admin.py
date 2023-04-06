from django.contrib import admin
from .models import Tourist, Link, Notice, VideoCate, VideoUpload


class NoticeAdmin(admin.ModelAdmin):
    list_display = ('level', 'release_time', 'detail')


class TouristAdmin(admin.ModelAdmin):
    list_display = ('IP', 'location', 'start_time', 'count', 'is_lock')


class LinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'link_url', 'link_img', 'add_time')
    search_fields = ('name', 'link_url')


class VideoCateAdmin(admin.ModelAdmin):
    list_display = ('name',)


class VideoUploadAdmin(admin.ModelAdmin):
    list_display = ('file', 'file_name', 'file_cate', 'create_time', 'comment')


admin.site.register(Notice, NoticeAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Tourist, TouristAdmin)
admin.site.register(VideoUpload, VideoUploadAdmin)
admin.site.register(VideoCate, VideoCateAdmin)
