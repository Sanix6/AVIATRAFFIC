import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = ['*']

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
    'apps.avia',
    'apps.users',
    'apps.home',
    'apps.notifications'

    
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',

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
        'HOST': os.getenv('HOST'),
        'PORT': os.getenv('PORT'),
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

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'drf_static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'drf_static/')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'


#other

EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = str(os.getenv('EMAIL_HOST_USER'))
EMAIL_HOST_PASSWORD = str(os.getenv('EMAIL_HOST_PASSWORD'))

REPORT_USER_EMAIL = os.getenv('REPORT_USER_EMAIL')
DEFAULT_FROM_EMAIL = os.getenv('RF')

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
        "link": {
            "decorators": [
                {
                    "model": "link",
                    "view": {
                        "name": "a",
                        "attributes": {"target": "_blank"}
                    },
                    "label": "Open in new tab",
                    "defaultValue": True
                }
            ]
        },
        "placeholder": "Start typing here...",
        "autogrow": True,
        "spellcheck": True,
        "language": "ru",
    }
}

CKEDITOR_UPLOAD_PATH = "uploads/"


ONE_SIGNAL_APP_ID  = os.getenv('APP_ID')
ONE_SIGNAL_REST = os.getenv('REST_API')


JAZZMIN_SETTINGS = {
    "site_logo": "Logo_avia.png",
    "site_brand": "AeroTraffic",
    "icons": {
        "home.Banner": "fas fa-image",
        "home.PopularDirection": "fas fa-map-marked-alt",
        "home.Category": "fas fa-th-list",
        "home.SubCategory": "fas fa-layer-group",

        "avia.Countries": "fas fa-flag",
        "avia.Cities": "fas fa-city",
        "avia.Airports": "fas fa-plane",

        "notifications.DeviceToken": "fas fa-mobile-alt",
        "notifications.Notifications": "fas fa-bell",

        "users.User": "fas fa-user",
    },
}
