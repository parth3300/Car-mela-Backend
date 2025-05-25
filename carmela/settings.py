import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

import cloudinary
cloudinary.config( 
  cloud_name = 'dal18b6wk',       # Replace with your cloud name
  api_key = '294982374822612',             # Replace with your API key
  api_secret = 'rQymIHFfvQ6-Cx36ZVh_NDvsf28'        # Replace with your API secret
)

SECRET_KEY = 'django-insecure-2uycd-ws$t(r*8)+=yl4vz$v+&4-=@1fe#mnbl4q3y(p^yrc%^'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'django_filters',
    'djoser',
    'corsheaders',

    # Cloudinary
    'cloudinary',
    'cloudinary_storage',

    # Your apps
    'store',
    'caruser',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'carmela.urls'

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

WSGI_APPLICATION = 'carmela.wsgi.application'
# Stripe settings

STRIPE_PUBLISHABLE_KEY = 'pk_test_51R7s8F09peBWzWCil0ounXGawkhl36OP6aaEfFtVCdp4MpsDTNpvfe6iaEqjr9ksSy3JcD8LLvlx0OehYtWvekCR00FLNBhdd2'
STRIPE_SECRET_KEY = "sk_test_51R7s8F09peBWzWCi6rEm8BcWJU0BOdjD2heuhjL3NWXPsMgzbd6SBdZN02kJLJbJJqnWFxzecnECxzMRqvTuVEur003En7iz3V" 
FRONTEND_URL = 'https://carmela-buy-and-sell-cars.vercel.app'
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '8edz5L#QmufhAeM',  # special character may cause issues if split dynamically
        'HOST': 'db.ymwdndsxjzkubwqgbsha.supabase.co',
        'PORT': '5432',
        'CONN_MAX_AGE': 600,
    }
}

# BASE_DIR = Path(__file__).resolve().parent.parent
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ✅ STATIC & MEDIA
STATIC_URL = '/static/'

if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# ✅ Cloudinary media storage
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dal18b6wk',
    'API_KEY': '294982374822612',
    'API_SECRET': 'rQymIHFfvQ6-Cx36ZVh_NDvsf28',  # Replace with real secret
}

# If you still want to use MEDIA_URL (optional but not needed for Cloudinary)
MEDIA_URL = '/media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'caruser.User'

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]

CORS_ALLOW_ALL_ORIGINS = True

REST_FRAMEWORK = {
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=500),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=555),
}

DJOSER = {
    'SERIALIZERS': {
        'user_create': 'caruser.serializers.UserCreateSerializer',
        'current_user': 'caruser.serializers.UserSerializer',
    }
}
