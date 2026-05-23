import pytest
import responses
from services.ugc.services.django_client import check_target_exists

@responses.activate
def test_check_target_exists_success():
    responses.add(responses.GET,"http://127.0.0.1:8000/api/v1/courses/objects/lesson/42/exists/",json={"exists":True},status=200)
    result=check_target_exists("lesson",42)
    assert result is True

@responses.activate
def test_check_target_exists_failure():
    responses.add(responses.GET,"http://127.0.0.1:8000/api/v1/courses/objects/lesson/42/exists/",json={"exists":False},status=200)
    result=check_target_exists("lesson",42)
    assert result is False