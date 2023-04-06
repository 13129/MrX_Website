from django.shortcuts import render

from apps.extension_tools.models import VideoUpload


def sum_all(request):  # 标签
    all_video = VideoUpload.objects.all()
    for al in all_video:
        print(al.screenshots_as_list)
    return render(request, "H_video.html", locals())


def video(request, video_url):
    get_video = VideoUpload.objects.get(file=video_url)
    return render(request, "video.html", locals())
