from shutil import rmtree as remove_content_recursively_from
from json import dump as dump_json
from pathlib import Path

from fastavro import writer, parse_schema


def resolve_storage_path(
    storage_directory: str,
    raw_or_stg: str,
    subdirectory: str,
    date: str,
) -> Path:
    file_storage = Path(storage_directory).resolve()
    if raw_or_stg in storage_directory and subdirectory in storage_directory:
        return file_storage
    return file_storage / raw_or_stg / subdirectory / date


def refresh_storage(storage_directory: Path) -> None:
    if storage_directory.exists():
        remove_content_recursively_from(storage_directory)
    storage_directory.mkdir(parents=True, exist_ok=True)


def generate_new_file(storage_directory: Path, date: str, file_format: str) -> Path:
    filename = f"{storage_directory.parent.name}_{date}.{file_format}"
    return storage_directory / filename


def store_data_as_json(file_path: Path, content: list[dict]) -> None:
    with file_path.open("w", encoding="utf-8") as file:
        dump_json(content, file, ensure_ascii=False, indent=4)


def store_data_as_avro(file_path: Path, content: list[dict], schema: dict) -> None:
    parsed_schema = parse_schema(schema)
    with file_path.open("wb") as file:
        writer(file, parsed_schema, content)


def provide_location_of_files_based_on(subdirectory_path: Path) -> str:
    return str(subdirectory_path.parent.parent.resolve())


def dump_to_raw_folder(
    content: list[dict],
    storage_directory: str,
    subdirectory: str,
    date: str,
) -> str:
    storage_path = resolve_storage_path(storage_directory, "raw", subdirectory, date)
    refresh_storage(storage_path)
    file_path = generate_new_file(storage_path, date, "json")

    store_data_as_json(file_path, content)

    return provide_location_of_files_based_on(storage_path)


def dump_to_stg_folder(
    content: list[dict],
    storage_directory: str,
    subdirectory: str,
    date: str,
    schema: dict,
) -> str:
    storage_path = resolve_storage_path(storage_directory, "stg", subdirectory, date)
    refresh_storage(storage_path)
    file_path = generate_new_file(storage_path, date, "avro")

    store_data_as_avro(file_path, content, schema)

    return provide_location_of_files_based_on(storage_path)
