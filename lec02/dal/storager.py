from shutil import rmtree as remove_content_recursively_from
from json import dump as dump_json
from pathlib import Path

from fastavro import writer, parse_schema


def resolve_path_to(storage_directory: str, storage_type: str) -> Path:
    file_storage = Path(storage_directory).resolve()
    return file_storage / storage_type


def refresh_storage(storage_directory: Path) -> None:
    if storage_directory.exists():
        remove_content_recursively_from(storage_directory)
    storage_directory.mkdir(parents=True, exist_ok=True)


def generate_new_filename(storage_directory: Path, date: str, file_format: str) -> Path:
    filename = f"sales_{date}.{file_format}"
    return storage_directory / filename


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
    date: str,
    schema: dict,
) -> str:
    storage_path = resolve_path_to(storage_directory, "stg")
    refresh_storage(storage_path)
    file_path = generate_new_filename(storage_path, date, "avro")

    store_data_as_avro(file_path, content, schema)

    return str(file_path)


def dump_to_raw_folder(
    content: list[dict],
    storage_directory: str,
    date: str,
) -> str:
    storage_path = resolve_path_to(storage_directory, "raw")
    refresh_storage(storage_path)
    file_path = generate_new_filename(storage_path, date, "json")

    store_data_as_json(file_path, content)

    return str(file_path)
