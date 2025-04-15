from shutil import rmtree as remove_content_recursively_from
from json import dump as dump_json
from pathlib import Path

from fastavro import writer, parse_schema


def locate_storage(
    storage_directory: str,
    raw_or_stg: str,
    subdirectory: str,
) -> Path:
    file_storage = Path(storage_directory).resolve()
    return file_storage / raw_or_stg / subdirectory


def refresh_storage(storage_directory: Path) -> None:
    if storage_directory.exists():
        remove_content_recursively_from(storage_directory)
    storage_directory.mkdir(parents=True, exist_ok=True)


def generate_new_filename(storage_directory: Path, date: str, file_format: str) -> Path:
    date_directory = storage_directory / date
    date_directory.mkdir(parents=True, exist_ok=True)
    filename = f"sales_{date}.{file_format}"
    return storage_directory / date / filename


def store_data_as_json(file_path: Path, content: list[dict]) -> None:
    with file_path.open("w", encoding="utf-8") as file:
        dump_json(content, file, ensure_ascii=False, indent=4)


def store_data_as_avro(file_path: Path, content: list[dict], schema: dict) -> None:
    parsed_schema = parse_schema(schema)
    with file_path.open("wb") as file:
        writer(file, parsed_schema, content)


def dump_to_stg_folder(
    content: list[dict],
    storage_directory: str,
    subdirectory: str,
    date: str,
    schema: dict,
) -> str:
    storage_path = locate_storage(storage_directory, "stg", subdirectory)
    refresh_storage(storage_path)
    file_path = generate_new_filename(storage_path, date, "avro")

    store_data_as_avro(file_path, content, schema)

    return str(file_path)


def dump_to_raw_folder(
    content: list[dict],
    storage_directory: str,
    subdirectory: str,
    date: str,
) -> str:
    storage_path = locate_storage(storage_directory, "raw", subdirectory)
    refresh_storage(storage_path)
    file_path = generate_new_filename(storage_path, date, "json")

    store_data_as_json(file_path, content)

    return str(file_path)
