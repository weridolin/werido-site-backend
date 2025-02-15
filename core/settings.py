"""
Django settings for weridoBlog project.

Generated by 'django-admin startproject' using Django 3.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from datetime import timedelta
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


env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
if not os.path.exists(env_file):
    print("can not find .env file...", env_file)
env.read_env(env_file,overrides=True)

print("read env success...",os.environ)
EMAIL_PWD = env('EMAIL_PWD')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = ['*']

# from django.contrib import 
# Application definition

INSTALLED_APPS = [
    # 'daphne', // 重写了 runserver命令,web服务用可twisted
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    # 'corsheaders',
    # "oauth2_provider",
    'django_filters',
    "channels", # 支持多种协议
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
    # "payment.apps.PaymentConfig"
    "django_grpc_framework"

]

# DJANGO CHANNELS
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}


MIDDLEWARE = [
    'middleswares.trace.OpenTracingMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS中间件
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.gzip.GZipMiddleware',

]

# # 跨域配置

CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie
CORS_ORIGIN_WHITELIST = [

    'http://127.0.0.1:3000',  # 允许的前端域名列表

]


CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'PATCH',
    'DELETE',
    'OPTIONS',
]


CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_EXPOSE_HEADERS = [
    'access-control-allow-origin',
    'access-control-allow-methods',
    'access-control-allow-credentials',

]



ROOT_URLCONF = 'core.urls'

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
# https://docs.djangoproject.com/en/3.1/ref/settings/#database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env("SITE_DATA_DB"),  # 数据库名称
        'USER': env("SITE_USER"),  # 拥有者，这个一般没修改
        'PASSWORD': env("SITE_PASSWORD"),  # 密码，自己设定的
        # # 默认的就没写
        'HOST': env("POSTGRES_HOST") if env("K8S") != "1" else f"{env('SITEDB_SVC_NAME')}.{env('SITEDB_SVC_NAME_NAMESPACE')}",
        'PORT': env("POSTGRES_PORT") if env("K8S") != "1" else f"{env('SITEDB_SVC_NAME_PORT')}",
    }
}

# cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        # "LOCATION": f"redis://:{os.environ.get('REDIS_PASSWORD','werido')}@{os.environ.get('REDIS_HOST','8.131.78.84')}:{os.environ.get('REDIS_PORT','6379')}/0",
        # "LOCATION": f"redis://:{os.environ.get('REDIS_PASSWORD','werido')}@localhost:6379/0",
        "LOCATION": f"redis://:{env('REDIS_PASSWORD')}@{env('REDIS_HOST')}:{env('REDIS_PORT')}/0" if env("K8S") != "1" else \
            f"redis://:{env('REDIS_PASSWORD')}@{env('REDIS_SVC_NAME')}.{env('REDIS_SVC_NAME_NAMESPACE')}:{env('REDIS_SVC_PORT')}/1",

        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "PASSWORD": "mysecret",
            "REDIS_CLIENT_CLASS": "redis.client.StrictRedis",
            "REDIS_CLIENT_KWARGS": {"decode_responses": True, "charset": "utf-8"},
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
LANGUAGE_CODE = 'zh-hans'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Shanghai'  # 修改时区

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
SESSION_COOKIE_AGE = 200


# CELERY ################3333
if env("K8S") != "1":
    CELERY_BROKER_URL = f"redis://:{env('REDIS_PASSWORD')}@{env('REDIS_HOST')}:{env('REDIS_PORT')}/1"
else:
    CELERY_BROKER_URL = f"redis://:{env('REDIS_PASSWORD')}@{env('REDIS_SVC_NAME')}.{env('REDIS_SVC_NAME_NAMESPACE')}:{env('REDIS_SVC_PORT')}/1"

CELERY_RESULT_BACKEND = CELERY_BROKER_URL
#: Only add pickle to this list if your broker is secured
#: from unwanted access (see userguide/security.html)
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'

from rest_framework_simplejwt.authentication import JWTAuthentication

# rest framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_simplejwt.authentication.JWTAuthentication',
        "authenticationV1.V1Authentication",

    ),
    'EXCEPTION_HANDLER': 'utils.exceptions.exceptions_handler',
    'DEFAULT_DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',  #
}


# oauth provider


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


# scrapy scripts

SPIDER_DIR = os.path.join(BASE_DIR, "scripts")


# jwt

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


# ETCD
ETCD_HOST = os.environ.get("ETCD_HOST", "etcd1")
ETCD_PORT = os.environ.get("ETCD_PORT", 2379)
USERCENTER_KEY = "/site/usercenter/rpc"


# srv in k8s
USERCENTER_SVC_NAME = os.environ.get("USERCENTER_SVC_NAME", None)
USERCENTER_SVC_NAME_NAMESPACE = os.environ.get(
    "USERCENTER_SVC_NAME_NAMESPACE", None)


# RabbitMq
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST", "siterabbitmq")

# jaeger
SERVICE_NAME = 'site-old-backend'

# OPENTRACING_TRACER_CONFIG = {
#     'sampler': {
#         'type': 'const',
#         'param': 1,
#     },
#     'local_agent': {
#         'reporting_host': 'jaeger',
#         'reporting_port': '4318',
#     },
#     'logging': True,
# }


JWT_KEY =  os.environ.get("JWT_KEY","DEBUGJWTKEY")