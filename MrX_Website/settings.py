"""
Django settings for MrX_Website project.

Generated by 'django-admin startproject' using Django 4.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
import sys
from pathlib import Path

from .simpleui_config import SIMPLEUI_CONFIG

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-hnezhga!%nii*)#)%8g6c+t3o19(kt(s%r7llb#22h+z6-^q4r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'imagekit',
    'apps.users',
    'apps.blogs',
    'apps.extension_tools',
    'apps.data_tools',
    'rest_framework',
    'mdeditor',
    'mptt',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MrX_Website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'MrX_Website.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

AUTH_USER_MODEL = 'users.Users'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# cache 开发调试缓存配置-
# CACHES = {
#     'default': {
#         # 'BACKEND': 'django.core.cache.backends.dummy.DummyCache',  # 缓存引擎
#         "BACKEND": 'django_redis.cache.RedisCache',
#         # 'LOCATION': 'redis://192.168.31.194:6379/3',
#         'LOCATION': 'redis://192.168.145.129:6379/3',
#         'TIMEOUT': 300,  # 缓存超时时间 None表示永不过期，0表示立即过期，默认300秒
#         'OPTIONS': {
#             # 'MAX_ENTRIES': 300,  # 最大缓存记录的数量（默认300）
#             # 'CULL_FREQUENCY': 3,  # 缓存到达最大个数之后，剔除缓存个数的比例，即：1/CULL_FREQUENCY（默认3）
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             # "PASSWORD": "8693",
#             "CONNECTION_POOL_KWARGS": {
#                 "max_connections": 100
#             }
#         },
#     }
# }
#
# # session保存在缓存中
# SESSION_ENGINE = "django.contrib.sessions.backends.cache"
# SESSION_CACHE_ALIAS = "default"
# SESSION_COOKIE_AGE = 80000  # 默认两周单位秒
# SESSION_COOKIE_HTTPONLY = True  # 设置session cookie是httponly
# SESSION_COOKIE_NAME = 'sessionId'  # session cookie的名字
# SESSION_COOKIE_PATH = '/'  # session cookie的path
# SESSION_COOKIE_SECURE = False  # session cookie的secure
# SESSION_SAVE_EVERY_REQUEST = True
# SESSION_EXPIRE_AT_BROWSER_CLOSE = True


# 菜单栏，图片查考
# https://element.eleme.cn/#/zh-CN/component/icon


SIMPLEUI_CONFIG = SIMPLEUI_CONFIG
SIMPLEUI_HOME_QUICK = False
SIMPLEUI_HOME_INFO = False
