from pytest import fixture
from lec02.extractor_job import app as job1
from lec02.loader_job import app as job2

from assertpy import assert_that


@fixture
def test_job1():
    job1.config["TESTING"] = True
    with job1.test_client() as test_client:
        yield test_client


@fixture
def test_job2():
    job2.config["TESTING"] = True
    with job2.test_client() as test_client:
        yield test_client


def test_missing_raw_dir_in_fileds(test_job1):
    response = test_job1.post(
        "/",
        json={"date": "2024-01-01"},
    )
    assert_that(response.status_code).is_equal_to(400)
    assert_that(response.json).contains_value(
        "Both raw_dir and date parameters should be provided!"
    )


def test_invalid_date_format(test_job1):
    response = test_job1.post(
        "/",
        json={"date": "19-19-1919", "raw_dir": "/some/path"},
    )
    assert_that(response.status_code).is_equal_to(400)
    assert_that(response.json).contains_value(
        "Date is in a wrong format! Must be 'YYYY-MM-DD'!"
    )


def test_directories_are_specified_wrongly(test_job2):
    response = test_job2.post(
        "/",
        json={"date": "2024-01-01", "raw_dir": "/some/path"},
    )
    assert_that(response.status_code).is_equal_to(400)
    assert_that(response.json).contains_value(
        "Both raw_dir and stg_dir parameters should be provided!"
    )


def test_no_raw_directory(test_job2):
    response = test_job2.post(
        "/",
        json={
            "raw_dir": "/some/none/existing/path",
            "stg_dir": "/yet/another/none/existing/path",
        }
    )
    assert_that(response.status_code).is_equal_to(404)
    assert_that(response.json["error"]).contains(
        "directory not found at:"
    )
