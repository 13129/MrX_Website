# Generated by Django 4.1.4 on 2023-03-30 04:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mdeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='文章类别')),
            ],
            options={
                'verbose_name': '文章类别',
                'verbose_name_plural': '文章类别',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='文章标签')),
            ],
            options={
                'verbose_name': '文章标签',
                'verbose_name_plural': '文章标签',
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('content', mdeditor.fields.MDTextField(verbose_name='正文')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('views', models.IntegerField(default=0, verbose_name='阅读量')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cate_blog', to='blogs.category', verbose_name='文章类别')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
                ('tags', models.ManyToManyField(to='blogs.tag', verbose_name='文章标签')),
            ],
            options={
                'verbose_name': '我的博客',
                'verbose_name_plural': '我的博客',
                'ordering': ['-update_time'],
            },
        ),
    ]