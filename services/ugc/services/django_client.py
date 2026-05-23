import os
import logging
import requests
from tenacity import retry, stop_after_attempt,wait_exponential,retry_if_exception_type
from services.ugc.common.exceptions import DjangoUnavailable
logger=logging.getLogger(__name__)

DJANGO_BASE_URL = os.getenv("DJANGO_BASE_URL","http://127.0.0.1:8000")

@retry(stop=stop_after_attempt(3),wait=wait_exponential(multiplier=1,min=1,max=5),retry=retry_if_exception_type(requests.RequestException),reraise=True)
def make_send_request(url:str)->requests.Response:
    """делаем запрос к django монолиту"""
    response = requests.get(url,timeout=2.0)
    logger.info("Отправлен get запрос")
    response.raise_for_status()
    return response


def check_target_exists(target_type: str, target_id: int)->bool:
    url = f"{DJANGO_BASE_URL}/api/v1/courses/objects/{target_type}/{target_id}/exists/"
    try:
        response = make_send_request(url)
        return response.json().get("exists",False)
    except requests.RequestException:
        raise DjangoUnavailable
