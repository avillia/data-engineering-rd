from pytest import fixture
from ..extractor_job import app

from assertpy import assert_that


@fixture
def test_client():
    app.config["TESTING"] = True
    with app.test_client() as test_client:
        yield test_client


def test_missing_raw_dir_in_fileds(test_client):
    response = test_client.post(
        "/",
        json={"date": "2024-01-01"},
    )
    assert_that(response.status_code).is_equal_to(400)
    assert_that(response.json).contains_value(
        "Both raw_dir and date parameters should be provided!"
    )


def test_invalid_date_format(test_client):
    """Should return 400 if date is in the wrong format"""
    response = test_client.post(
        "/",
        json={"date": "19-19-1919", "raw_dir": "/some/path"},
    )
    assert_that(response.status_code).is_equal_to(400)
    assert_that(response.json).contains_value(
        "Date is in a wrong format! Must be 'YYYY-MM-DD'!"
    )
