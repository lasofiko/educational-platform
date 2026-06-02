import pytest
import responses

from services.ugc.services.django_client import check_target_exists

@responses.activate
def test_check_target_exists_success(app, django_exists_url):
    responses.add(responses.GET, django_exists_url("lesson", 42), json={"exists": True}, status=200)
    result = check_target_exists("lesson", 42)
    assert result is True

@responses.activate
def test_check_target_exists_failure(app, django_exists_url):
    responses.add(responses.GET, django_exists_url("lesson", 42), json={"exists": False}, status=200)
    result = check_target_exists("lesson", 42)
    assert result is False