import os
import logging
import requests
from tenacity import retry, stop_after_attempt,wait_exponential,retry_if_exception_type
from services.ugc.common.exceptions import DjangoUnavailable
from services.ugc.common.exceptions import TargetNotFound
logger=logging.getLogger(__name__)

def _django_base_url() -> str:
    return os.environ.get("DJANGO_BASE_URL", "http://127.0.0.1:8000").rstrip("/")

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=5),
    retry=retry_if_exception_type(requests.RequestException),
    reraise=True,
)
def make_send_request(url: str) -> requests.Response:
    response = requests.get(url, timeout=2.0)
    logger.info("Отправлен get запрос")

    if response.status_code == 404:
        return response
    response.raise_for_status()
    return response


def check_target_exists(target_type: str, target_id: int, base_url: str | None = None) -> bool:
    base = (base_url or _django_base_url()).rstrip("/")
    url = f"{base}/api/v1/courses/objects/{target_type}/{target_id}/exists/"
    try:
        response = make_send_request(url)
    except requests.RequestException:
        raise DjangoUnavailable()

    if response.status_code == 404:
        return False

    if response.status_code != 200:
        raise DjangoUnavailable()

    return response.json().get("exists", False)

class DjangoClient:
    """Обёртка для UGCService и blueprints: bool Матвея → исключение для API."""

    def __init__(self, base_url=None, timeout=2.0):
        self._base_url = base_url
        self.timeout = timeout

    @property
    def base_url(self):
        if self._base_url is not None:
            return self._base_url.rstrip("/")
        return _django_base_url()

    def check_target_exists(self, target_type: str, target_id: int) -> None:
        if not check_target_exists(target_type, target_id, base_url=self.base_url):
            raise TargetNotFound(target_type, target_id)