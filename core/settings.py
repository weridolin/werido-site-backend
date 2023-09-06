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
import environ

# initialize env
env = environ.Env(
    # # set casting, default value
    # DEBUG=(bool, False)
)
# reading .env file


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


if not os.path.exists(os.path.join(os.path.dirname(BASE_DIR),".env")):
    print("can not find .env file...",os.path.join(os.path.dirname(BASE_DIR),".env"))

    
environ.Env.read_env(os.path.join(os.path.dirname(BASE_DIR),".env"))

EMAIL_PWD = env('EMAIL_PWD')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    # "oauth2_provider",
    'django_filters',
    "channels",
    "django_celery_beat",
    "rest_framework_simplejwt.token_blacklist",

    # 'authentication.apps.AuthenticationConfig',     # 移动到usercenter
    "thirdApis.apps.ThirdapisConfig",
    # "rbac.apps.RbacConfig", # 移动到usercenter
    'articles.apps.ArticlesConfig',
    'drug.apps.DrugConfig',
    'home.apps.HomeConfig',
    "filebroker.apps.FilebrokerConfig",
    "celery_app.apps.CeleryAppConfig",
    "dataFaker.apps.DatafakerConfig",
    # 'oauth.apps.OauthConfig',
    "covid19.apps.Covid19Config",
    "wechat.apps.WechatConfig",
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
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8000',
    'http://127.0.0.1:8888',
    'http://localhost:8000',
    'http://localhost:8080',
    'http://localhost:8085',
    'http://localhost:8888',
    'http://localhost:3000',
    'http://localhost:8081', #凡是出现在白名单中的域名，都可以访问后端接口
)

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

######################################  Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

print( env("POSTGRES_HOST"),">>>>>")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("POSTGRES_DB"),  # 数据库名称
        'USER': env("POSTGRES_USER"),  # 拥有者，这个一般没修改
        'PASSWORD': env("POSTGRES_PASSWORD"),  # 密码，自己设定的
        'HOST': env("POSTGRES_HOST"),  # 默认的就没写
        'PORT': env("POSTGRES_PORT"),        
        # 'HOST': 'sitedb',
        # 'PORT': '5432',
    }
}

######################################### cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # "LOCATION": f"redis://:{os.environ.get('REDIS_PASSWORD','werido')}@{os.environ.get('REDIS_HOST','8.131.78.84')}:{os.environ.get('REDIS_PORT','6379')}/0",
        # "LOCATION": f"redis://:{os.environ.get('REDIS_PASSWORD','werido')}@localhost:6379/0",
        "LOCATION": f"redis://:{env('REDIS_PASSWORD')}@{env('REDIS_HOST')}:{env('REDIS_PORT')}/0",
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

# 日志相关地址
LOG_URL = '/logs/'
LOG_ROOT = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_ROOT):
    os.makedirs(LOG_ROOT)

# 过期时间
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 200 #


############## CELERY ################3333
CELERY_BROKER_URL =  f"redis://:{env('REDIS_PASSWORD')}@{env('REDIS_HOST')}:{env('REDIS_PORT')}/1"
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'



########################### rest framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        
    ),
    'EXCEPTION_HANDLER': 'utils.exceptions.exceptions_handler',
    'DEFAULT_DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',  #
}


################# oauth provider


# OAUTH2_PROVIDER = {
#     'ACCESS_TOKEN_EXPIRE_SECONDS': 3600,
#     # 'SCOPES_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore',
#     'APPLICATION_MODEL': 'oauth.OauthApplicationModel',
#     'ACCESS_TOKEN_MODEL': 'oauth.AccessTokenModel',
#     # "ACCESS_TOKEN_GENERATOR": "oauth.utils.oauth_token_generator"
# }
# OAUTH2_PROVIDER_APPLICATION_MODEL = 'oauth.OauthApplicationModel'
# OAUTH2_PROVIDER_ACCESS_TOKEN_MODEL = 'oauth.AccessTokenModel'
# OAUTH2_PROVIDER_REFRESH_TOKEN_MODEL = "oauth.RefreshTokenModel"
# OAUTH2_PROVIDER_ID_TOKEN_MODEL = "oauth.IDTokenModel"
# OAUTH2_PROVIDER_GRANT_MODEL= "oauth.OauthGrantModel"



################## scrapy scripts 

SPIDER_DIR = os.path.join(BASE_DIR,"scripts")




####################### jwt
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=6),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=3),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


########### ETCD
ETCD_HOST = os.environ.get("ETCD_HOST","etcd1")
ETCD_PORT = os.environ.get("ETCD_PORT",2379)
USERCENTER_KEY = "/site/usercenter/rpc"


############ RabbitMq
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST","siterabbitmq")