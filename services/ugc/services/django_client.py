import os

import requests

from services.ugc.common.exceptions import DjangoUnavailable, TargetNotFound


class DjangoClient:
    def __init__(self, base_url=None, timeout=1.0):
        self._base_url = base_url
        self.timeout = timeout

    @property
    def base_url(self):
        if self._base_url is not None:
            return self._base_url.rstrip('/')
        return os.environ.get('DJANGO_BASE_URL', 'http://localhost:8000').rstrip('/')

    def check_target_exists(self, target_type: str, target_id: int) -> None:
        url = f'{self.base_url}/api/v1/courses/objects/{target_type}/{target_id}/exists/'
        try:
            response = requests.get(url, timeout=self.timeout)
        except requests.RequestException as exc:
            raise DjangoUnavailable() from exc

        if response.status_code == 404:
            raise TargetNotFound(target_type, target_id)

        if response.status_code != 200:
            raise TargetNotFound(target_type, target_id)

        payload = response.json()
        if not payload.get('exists'):
            raise TargetNotFound(target_type, target_id)