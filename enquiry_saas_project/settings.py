from pathlib import Path
import os
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6r7wz)=6f#w9v5dc7#a7@*aro%-n+wh(iz17(7zd#&^7uh6*db'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []
RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# Application definition

INSTALLED_APPS = [
    "jet",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rangefilter",
    "import_export",
    "cloudinary",
    "cloudinary_storage",
    # My Apps
    "sales_enquiry",
    "crispy_forms",
    "crispy_bootstrap5",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = 'enquiry_saas_project.urls'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"  # Add this
CRISPY_TEMPLATE_PACK = "bootstrap5"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],  # Add this line
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = 'enquiry_saas_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(
        default="sqlite:///db.sqlite3",  # This is your local fallback, ignored on Render if DATABASE_URL is set
        conn_max_age=600,  # Optional: Reconnect after 10 minutes of inactivity
    )
}

CLOUDINARY = {
    "cloud_name": os.environ.get("CLOUDINARY_CLOUD_NAME", "YOUR_CLOUD_NAME"),
    "api_key": os.environ.get("CLOUDINARY_API_KEY", "YOUR_API_KEY"),
    "api_secret": os.environ.get("CLOUDINARY_API_SECRET", "YOUR_API_SECRET"),
}

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True

USE_I18N = True
USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

CSRF_TRUSTED_ORIGINS = ["https://*.render.com"]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),  # Add this line
]

JET_SETTINGS = {
    "MENU_SHOW_MODULES": True,  # Show individual models in the menu
    "SITE_HEADER": "Enquiry Management System",
    "MENU_INCLUDE_APPS": [
        "sales_enquiry",
        "auth",
    ],  # Only include these apps in the menu
    "MENU_EXCLUDE_APPS": [],
    # 'THEME': 'light-blue', # Default is 'light-blue'. Other options might exist, check docs
    "CHANGE_FORM_SUBMIT_ON_ENTER": False,  # Prevent form submission on Enter key
    "SIDEBAR_COMPACT": False,  # Make sidebar compact
    "TOOLBAR_DENSE": False,  # Make toolbar dense
    "BRAND_TEXT": "Enquiry Admin",  # Text in the header
    "DEFAULT_APP_ICON": "fa fa-folder-o",  # Font Awesome icon for apps
    "DEFAULT_MODEL_ICON": "fa fa-file-o",  # Font Awesome icon for models
    # Refer to Django JET Reboot documentation for more extensive options:
    # https://github.com/jet-admin/django-jet-reboot#settings (or their official docs)
}

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

LOGIN_REDIRECT_URL = "/dse/dashboard/"  # Redirect DSEs to their dashboard after login
LOGOUT_REDIRECT_URL = "/"  # Redirect to home page after logout

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = "sales_enquiry.CustomUser"
