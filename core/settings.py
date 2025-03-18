from pathlib import Path
import os

from django.conf.global_settings import AUTH_USER_MODEL

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'django-insecure-)l%w14$hgye-7v5eksw@gr=ahihf5ryy%#%#d&*=ftn)tpqn^='

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'django_ckeditor_5',

    #apps
    'apps.users',
    'apps.home'

    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'


#database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': 'localhost', 
        'PORT': '5432',
    }
}



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

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'drf_static/'
MEDIA_URL = 'media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'drf_static/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'


#other

EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')


SPECTACULAR_SETTINGS = {
    'TITLE': 'AERO TRAFFIC',
    'DESCRIPTION': '',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

UNFOLD = {
    "THEME": "slate", # "light", "dark", "slate"
    "COLOR": {
        "primary": "#4A90E2",  # основной цвет
        "secondary": "#E94E77",  # вторичный цвет
        "accent": "#FF5733",  # акцентный цвет
        "background": "#F4F4F4",  # цвет фона
        "button": "#007BFF",  # цвет кнопок
        "text": "#333333"
    },
}

CKEDITOR_5_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"


CKEDITOR_5_CONFIGS = {
    'default': {
        "toolbar": [
            "heading", "|", "bold", "italic", "underline", "|",
            "link", "blockquote", "codeBlock", "imageUpload", "|",
            "bulletedList", "numberedList", "todoList", "|",
            "outdent", "indent", "|",
            "sourceEditing"
        ],
        "image": {
            "toolbar": [
                "imageTextAlternative", "|",
                "imageStyle:alignLeft", "imageStyle:full", "imageStyle:alignRight"
            ],
            "styles": ["full", "alignLeft", "alignRight"]
        },
        "table": {
            "contentToolbar": [
                "tableColumn", "tableRow", "mergeTableCells"
            ]
        },
        "mediaEmbed": {
            "previewsInData": True
        },
    }
}


CKEDITOR_UPLOAD_PATH = "uploads/"