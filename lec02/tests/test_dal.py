from assertpy import assert_that

from dal.extractor import dump_to_folder


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
    storage = dump_to_folder(fake_data)
    assert_that(storage).is_file()
    assert_that(storage).is_not_empty()
