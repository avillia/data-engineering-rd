from json import load as read_json_from
from pathlib import Path
from shutil import rmtree as remove_content_recursively_from

from assertpy import assert_that
from fastavro import reader
from pytest import fixture

from lec02.dal.storager import (
    dump_to_raw_folder,
    dump_to_stg_folder,
    refresh_storage,
)


@fixture
def temporary_storage():
    test_storage = Path("../test_storage").resolve()
    test_storage.mkdir(parents=True)
    yield test_storage

    ...

    remove_content_recursively_from(test_storage)


def create_dummy_json_file_inside(target_dir: Path, identifier: int) -> None:
    fake_data = "We do not care about contents of those files"
    file_path = target_dir / f"test_file_{identifier}"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(fake_data)


def test_storage_directory_is_cleaned_up_on_refresh(temporary_storage: Path):
    create_dummy_json_file_inside(temporary_storage, 1)
    create_dummy_json_file_inside(temporary_storage, 2)
    create_dummy_json_file_inside(temporary_storage, 3)
    create_dummy_json_file_inside(temporary_storage, 4)

    directory_contents_before_cleanup = list(temporary_storage.iterdir())
    assert_that(directory_contents_before_cleanup).is_not_empty()

    refresh_storage(temporary_storage)
    directory_contents_after_cleanup = list(temporary_storage.iterdir())
    assert_that(directory_contents_after_cleanup).is_empty()


def test_json_file_is_created_correctly(temporary_storage: Path):
    fake_data = [
        {
            "client": "Michael Wilkerson",
            "purchase_date": "2022-08-09",
            "product": "Vacuum cleaner",
            "price": 346,
        },
        {
            "client": "Russell Hill",
            "purchase_date": "2022-08-09",
            "product": "Microwave oven",
            "price": 446,
        },
        {
            "client": "Michael Galloway",
            "purchase_date": "2022-08-09",
            "product": "Phone",
            "price": 1042,
        },
    ]
    raw_dir = temporary_storage / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    storage = dump_to_raw_folder(fake_data, str(raw_dir), "2022-08-09")

    assert_that(storage).is_not_empty()
    assert_that(storage).is_file()

    with open(storage, "r", encoding="utf-8") as file:
        written_data = read_json_from(file)
        assert_that(written_data).is_equal_to(fake_data)


def test_avro_file_is_created_correctly(temporary_storage: Path):
    fake_data = [
        {
            "product": "Vacuum cleaner",
            "price": 346,
        },
        {
            "product": "Microwave oven",
            "price": 446,
        },
        {
            "product": "Phone",
            "price": 1042,
        },
    ]

    schema = {
        "doc": "Test product data.",
        "name": "product",
        "namespace": "test",
        "type": "record",
        "fields": [
            {"name": "product", "type": "string"},
            {"name": "price", "type": "int"},
        ],
    }

    stg_dir = temporary_storage / "raw"
    stg_dir.mkdir(parents=True, exist_ok=True)
    storage = dump_to_stg_folder(fake_data, str(stg_dir), "2022-08-09", schema)

    assert_that(storage).is_not_empty()
    assert_that(storage).is_file()

    with open(storage, "rb") as file:
        written_data = reader(file)
        assert_that(list(written_data)).is_equal_to(fake_data)
