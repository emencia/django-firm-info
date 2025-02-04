"""
Base Django settings for sandbox
"""

from pathlib import Path


SECRET_KEY = "***TOPSECRET***"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Root of project repository
BASE_DIR = Path(__file__).parents[2]

# Django project
PROJECT_PATH = BASE_DIR / "sandbox"

# Variable content directory, mostly use for local db and media storage in
# deployed environments
VAR_PATH = BASE_DIR / "var"

DEBUG = False

# Https is never enabled on default and development environment, only for
# integration and production.
HTTPS_ENABLED = False

ADMINS = (
    # ("Admin", "PUT_ADMIN_EMAIL_HERE"),
)

MANAGERS = ADMINS

DATABASES = {}

MIGRATION_MODULES = {}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]

# Local time zone for this installation
TIME_ZONE = "UTC"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en"

LANGUAGES = (
    ("en", "English"),
    ("fr", "Français"),
)

# A tuple of directories where Django looks for translation files
LOCALE_PATHS = [
    PROJECT_PATH / "locale",
]

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = VAR_PATH / "media"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = "/media/"

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = VAR_PATH / "static"

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = "/static/"

# Additional locations of static files
STATICFILES_DIRS = [
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_PATH / "static-sources",
]


MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
]

ROOT_URLCONF = "sandbox.urls"

# Python dotted path to the WSGI application used by Django"s runserver.
WSGI_APPLICATION = "sandbox.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            PROJECT_PATH / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "debug": False,
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sites",
    "django.contrib.staticfiles",
    "django.forms",
]

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Ensure we can override applications widgets templates from project template
# directory, require also 'django.forms' in INSTALLED_APPS
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

"""
Text editor configuration

Lotus plugin itself does not use editor this is only for DjangoCMS usage.

We safely try to use the one from 'djangocms_text' if available else
'djangocms_text_ckeditor' and finally if none of these are available we don't install
any apps since we fallback to the builtin Django Textarea widget.
"""
try:
    import djangocms_text  # noqa: F401,F403
except ImportError:
    try:
        import djangocms_text_ckeditor  # noqa: F401,F403
    except ImportError:
        # Application will use Django Textarea widget
        pass
    else:
        INSTALLED_APPS.extend([
            "djangocms_text_ckeditor",
        ])
else:
    INSTALLED_APPS.extend([
        "djangocms_text",
        "djangocms_text.contrib.text_ckeditor4",
    ])

    TEXT_EDITOR = "djangocms_text.contrib.text_ckeditor4.ckeditor4"
    # We don't enable cms so there is no need of its models
    MIGRATION_MODULES["djangocms_text"] = None


"""
Django smart media configuration using its defaults
"""
from smart_media.settings import *  # noqa: E402,F401,F403

INSTALLED_APPS.extend([
    "sorl.thumbnail",
    "smart_media",
])


"""
firm_info configuration using its defaults
"""
from firm_info.defaults import *  # noqa: E402,F401,F403

INSTALLED_APPS.extend([
    "firm_info",
])
