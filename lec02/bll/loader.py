from lec02.dal.converter import convert_json_to_avro
from lec02.dal.reader import read_raw_files_from
from lec02.dal.storager import dump_to_stg_folder


SCHEMA = {
    "doc": "Sales data",
    "name": "Sales",
    "namespace": "test",
    "type": "record",
    "fields": [
        {"name": "client", "type": "string"},
        {"name": "purchase_date", "type": {"type": "int", "logicalType": "date"}},
        {"name": "product", "type": "string"},
        {"name": "price", "type": "int"},
    ],
}


def convert_data_to_stg_format(raw_dir: str, stg_dir: str) -> str:
    data_per_date = read_raw_files_from(raw_dir, "sales")
    if not data_per_date:
        raise ValueError("Nothing to convert, raw directory is empty!")

    for date in data_per_date:
        json_contents = data_per_date[date]
        avro_contents = convert_json_to_avro(json_contents)
        file_storage = dump_to_stg_folder(
            avro_contents,
            stg_dir,
            "sales",
            date,
            SCHEMA,
        )
    return file_storage
