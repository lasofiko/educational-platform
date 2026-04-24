INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
    "django_filters",
    # Local apps
    "courses",
    "accounts",
    "progress",
]



INSTALLED_APPS += [
    'django_app.common',
]


REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'django_app.common.exception_handler.common_exception_handler',
}