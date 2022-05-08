"""
Django settings for weridoBlog project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '2h+r=ch3g(m9w!1fg_zk_le)g@&qalpb8b%k4+8z)r(pfx&brk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG",True)

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'articles.apps.ArticlesConfig',
    'drug.apps.DrugConfig',
    'home.apps.HomeConfig',
    "filebroker.apps.FilebrokerConfig",
    "celery_app.apps.CeleryAppConfig",
    "dataFaker.apps.DatafakerConfig",
    'rest_framework',
    'corsheaders',
    'authentication',
    'django_filters',
    "channels",

]

########## DJANGO CHANNELS
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}




MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

# # 跨域配置
# CORS_ORIGIN_WHITELIST = (
#     'http://127.0.0.1:8000',
#     'http://127.0.0.1:8888',
#     'http://localhost:8000',
#     'http://localhost:8080',
#     'http://localhost:8085',
#     'http://localhost:8888',
#     'http://localhost:8081', #凡是出现在白名单中的域名，都可以访问后端接口
# )

CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie

ROOT_URLCONF = 'core.urls'

import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get("POSTGRES_DB",'blogDB'),  # 数据库名称
        'USER': os.environ.get("POSTGRES_USER",'werido'),  # 拥有者，这个一般没修改
        'PASSWORD': os.environ.get("POSTGRES_PASSWORD",359066432),  # 密码，自己设定的
        'HOST': os.environ.get("POSTGRES_HOST",'8.131.78.84'),  # 默认的就没写
        'PORT': os.environ.get("POSTGRES_PORT",'5432'),
        # 'HOST': 'sitedb',
        # 'PORT': '5432',
    }
}


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://:{os.environ.get('REDIS_PASSWORD','werido')}@{os.environ.get('REDIS_HOST','8.131.78.84')}:{os.environ.get('REDIS_PORT','6379')}/0",
        # "LOCATION": f"redis://:{os.environ.get('REDIS_PASSWORD','werido')}@localhost:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "PASSWORD": "mysecret",
            "REDIS_CLIENT_CLASS": "redis.client.StrictRedis",
            "REDIS_CLIENT_KWARGS": {"decode_responses": True, "charset":"utf-8"},
            
        }
    },
    # "redis":{
    #     "BACKEND": "django_redis.cache.RedisCache",
    #     "LOCATION": f"redis://:{os.environ.get('redis_password','tianji')}@localhost:6379/0",
    #     "OPTIONS": {
    #         "CLIENT_CLASS": "django_redis.client.DefaultClient",
    #     }
    # },
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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

ADMIN_SITE_HEADER = 'werido blog'
# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/
# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE ='zh-hans'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'  ##修改时区

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# 媒体文件地址
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

print(MEDIA_ROOT)

# 过期时间
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 200 #


############## CELERY ################3333
CELERY_BROKER_URL = f"redis://:{os.environ.get('REDIS_PASSWORD','werido')}@{os.environ.get('REDIS_HOST','127.0.0.1')}:{os.environ.get('REDIS_PORT','6379')}/0"
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'