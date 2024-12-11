"""
Django settings for EBAsite project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-pp7fg00gzn!nx09s5z-3=(ztsq+jn3=w3o11_0_1k_xd9a)#x4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Application definition

INSTALLED_APPS = [
    'EBDashBoard.apps.EbdashboardConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "allauth",
    "allauth.account",
    "allauth.mfa",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.agave",
    "allauth.socialaccount.providers.amazon",
    "allauth.socialaccount.providers.amazon_cognito",
    "allauth.socialaccount.providers.angellist",
    "allauth.socialaccount.providers.apple",
    "allauth.socialaccount.providers.asana",
    "allauth.socialaccount.providers.atlassian",
    "allauth.socialaccount.providers.auth0",
    "allauth.socialaccount.providers.authentiq",
    "allauth.socialaccount.providers.baidu",
    "allauth.socialaccount.providers.basecamp",
    "allauth.socialaccount.providers.battlenet",
    "allauth.socialaccount.providers.bitbucket_oauth2",
    "allauth.socialaccount.providers.bitly",
    "allauth.socialaccount.providers.box",
    "allauth.socialaccount.providers.cilogon",
    "allauth.socialaccount.providers.clever",
    "allauth.socialaccount.providers.coinbase",
    "allauth.socialaccount.providers.dataporten",
    "allauth.socialaccount.providers.daum",
    "allauth.socialaccount.providers.digitalocean",
    "allauth.socialaccount.providers.dingtalk",
    "allauth.socialaccount.providers.discord",
    "allauth.socialaccount.providers.disqus",
    "allauth.socialaccount.providers.douban",
    "allauth.socialaccount.providers.doximity",
    "allauth.socialaccount.providers.draugiem",
    "allauth.socialaccount.providers.drip",
    "allauth.socialaccount.providers.dropbox",
    "allauth.socialaccount.providers.dummy",
    "allauth.socialaccount.providers.dwolla",
    "allauth.socialaccount.providers.edmodo",
    "allauth.socialaccount.providers.edx",
    "allauth.socialaccount.providers.eventbrite",
    "allauth.socialaccount.providers.eveonline",
    "allauth.socialaccount.providers.evernote",
    "allauth.socialaccount.providers.exist",
    "allauth.socialaccount.providers.facebook",
    "allauth.socialaccount.providers.feedly",
    "allauth.socialaccount.providers.figma",
    "allauth.socialaccount.providers.fivehundredpx",
    "allauth.socialaccount.providers.flickr",
    "allauth.socialaccount.providers.foursquare",
    "allauth.socialaccount.providers.frontier",
    "allauth.socialaccount.providers.fxa",
    "allauth.socialaccount.providers.gitea",
    "allauth.socialaccount.providers.github",
    "allauth.socialaccount.providers.gitlab",
    "allauth.socialaccount.providers.globus",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.gumroad",
    "allauth.socialaccount.providers.hubic",
    "allauth.socialaccount.providers.hubspot",
    "allauth.socialaccount.providers.instagram",
    "allauth.socialaccount.providers.jupyterhub",
    "allauth.socialaccount.providers.kakao",
    "allauth.socialaccount.providers.lemonldap",
    "allauth.socialaccount.providers.lichess",
    "allauth.socialaccount.providers.line",
    "allauth.socialaccount.providers.linkedin_oauth2",
    "allauth.socialaccount.providers.mailchimp",
    "allauth.socialaccount.providers.mailru",
    "allauth.socialaccount.providers.mediawiki",
    "allauth.socialaccount.providers.meetup",
    "allauth.socialaccount.providers.microsoft",
    "allauth.socialaccount.providers.miro",
    "allauth.socialaccount.providers.naver",
    "allauth.socialaccount.providers.netiq",
    "allauth.socialaccount.providers.nextcloud",
    "allauth.socialaccount.providers.notion",
    "allauth.socialaccount.providers.odnoklassniki",
    "allauth.socialaccount.providers.openid",
    "allauth.socialaccount.providers.openid_connect",
    "allauth.socialaccount.providers.openstreetmap",
    "allauth.socialaccount.providers.orcid",
    "allauth.socialaccount.providers.patreon",
    "allauth.socialaccount.providers.paypal",
    "allauth.socialaccount.providers.pinterest",
    "allauth.socialaccount.providers.pocket",
    "allauth.socialaccount.providers.questrade",
    "allauth.socialaccount.providers.quickbooks",
    "allauth.socialaccount.providers.reddit",
    "allauth.socialaccount.providers.robinhood",
    "allauth.socialaccount.providers.salesforce",
    "allauth.socialaccount.providers.saml",
    "allauth.socialaccount.providers.sharefile",
    "allauth.socialaccount.providers.shopify",
    "allauth.socialaccount.providers.slack",
    "allauth.socialaccount.providers.snapchat",
    "allauth.socialaccount.providers.soundcloud",
    "allauth.socialaccount.providers.spotify",
    "allauth.socialaccount.providers.stackexchange",
    "allauth.socialaccount.providers.steam",
    "allauth.socialaccount.providers.stocktwits",
    "allauth.socialaccount.providers.strava",
    "allauth.socialaccount.providers.stripe",
    "allauth.socialaccount.providers.telegram",
    "allauth.socialaccount.providers.tiktok",
    "allauth.socialaccount.providers.trainingpeaks",
    "allauth.socialaccount.providers.trello",
    "allauth.socialaccount.providers.tumblr",
    "allauth.socialaccount.providers.twentythreeandme",
    "allauth.socialaccount.providers.twitch",
    "allauth.socialaccount.providers.twitter",
    "allauth.socialaccount.providers.twitter_oauth2",
    "allauth.socialaccount.providers.untappd",
    "allauth.socialaccount.providers.vimeo",
    "allauth.socialaccount.providers.vimeo_oauth2",
    "allauth.socialaccount.providers.vk",
    "allauth.socialaccount.providers.wahoo",
    "allauth.socialaccount.providers.weibo",
    "allauth.socialaccount.providers.weixin",
    "allauth.socialaccount.providers.windowslive",
    "allauth.socialaccount.providers.xing",
    "allauth.socialaccount.providers.yahoo",
    "allauth.socialaccount.providers.yandex",
    "allauth.socialaccount.providers.ynab",
    "allauth.socialaccount.providers.zoho",
    "allauth.socialaccount.providers.zoom",
    "allauth.socialaccount.providers.okta",
    "allauth.socialaccount.providers.feishu",
    "allauth.usersessions",
    "allauth.headless",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'EBAsite.urls'
LOGIN_URL = "/accounts/login/"
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'EBAsite.wsgi.application'
TIME_ZONE = 'Asia/Shanghai'
# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'mongodb': {
        'ENGINE': 'mongoengine.django.storage.StorageEngine',
        'NAME': 'E_Business_data',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "zh-hans"

LANGUAGES = [
    ("ar", "Arabic"),
    ("az", "Azerbaijani"),
    ("bg", "Bulgarian"),
    ("ca", "Catalan"),
    ("cs", "Czech"),
    ("da", "Danish"),
    ("de", "German"),
    ("el", "Greek"),
    ("en", "English"),
    ("es", "Spanish"),
    ("et", "Estonian"),
    ("eu", "Basque"),
    ("fa", "Persian"),
    ("fi", "Finnish"),
    ("fr", "French"),
    ("he", "Hebrew"),
    ("hr", "Croatian"),
    ("hu", "Hungarian"),
    ("id", "Indonesian"),
    ("it", "Italian"),
    ("ja", "Japanese"),
    ("ka", "Georgian"),
    ("ko", "Korean"),
    ("ky", "Kyrgyz"),
    ("lt", "Lithuanian"),
    ("lv", "Latvian"),
    ("mn", "Mongolian"),
    ("nb", "Norwegian Bokmål"),
    ("nl", "Dutch"),
    ("pl", "Polish"),
    ("pt-BR", "Portuguese (Brazil)"),
    ("pt-PT", "Portuguese (Portugal)"),
    ("ro", "Romanian"),
    ("ru", "Russian"),
    ("sk", "Slovak"),
    ("sl", "Slovenian"),
    ("sr", "Serbian"),
    ("sr-Latn", "Serbian (Latin)"),
    ("sv", "Swedish"),
    ("th", "Thai"),
    ("tr", "Turkish"),
    ("uk", "Ukrainian"),
    ("zh-hans", "Chinese (Simplified)"),
    ("zh-hant", "Chinese (Traditional)"),
]

USE_I18N = True

USE_TZ = True

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
