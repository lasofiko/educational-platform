import os
from pathlib import Path
from split_settings.tools import include

BASE_DIR = Path(__file__).resolve().parent.parent

include(
    "components/base_settings.py",
    "components/security.py",
    "components/apps.py",
    "components/middlewares.py",
    "components/templates.py",
    "components/databases.py",
    "components/validators.py",
    "components/internationalization.py",
    "components/static.py",
)


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


