from json import dump as dump_json
from json import load as read_json_from
from pathlib import Path
from shutil import rmtree as remove_content_recursively_from

from assertpy import assert_that

from dal.storager import dump_to_folder, resolve_path_to, refresh_storage


def create_dummy_json_file_inside(target_dir: Path, identifier: int) -> None:
    fake_data = {
            "client": "We do not care",
            "purchase_date": "about whatever",
            "product": "are contents here",
            "price": identifier * 200,
        },
    file_path = target_dir / f"test_file_{identifier}.json"
    with open(file_path, "w", encoding="utf-8") as file:
        dump_json(fake_data, file)


def test_storage_directory_is_cleaned_up_on_refresh():
    test_storage: Path = resolve_path_to("../test_storage")
    test_storage.mkdir(parents=True, exist_ok=True)

    create_dummy_json_file_inside(test_storage, 1)
    create_dummy_json_file_inside(test_storage, 2)
    create_dummy_json_file_inside(test_storage, 3)
    create_dummy_json_file_inside(test_storage, 4)
    directory_contents_before_cleanup = list(test_storage.iterdir())
    assert_that(directory_contents_before_cleanup).is_not_empty()

    refresh_storage(test_storage)
    directory_contents_after_cleanup = list(test_storage.iterdir())
    assert_that(directory_contents_after_cleanup).is_empty()

    test_storage.rmdir()


def test_file_is_created_correctly():
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
    storage = dump_to_folder(fake_data, "../test_storage/raw")
    assert_that(storage).is_file()
    assert_that(storage).is_not_empty()

    with open(storage, "r", encoding="utf-8") as file:
        written_data = read_json_from(file)
        assert_that(written_data).is_equal_to(fake_data)

    remove_content_recursively_from(Path(storage).resolve().parent.parent)