from shutil import rmtree as remove_content_recursively_from
from json import dump as dump_json
from pathlib import Path


def resolve_path_to(storage_directory: str) -> Path:
    return Path(storage_directory).resolve()


def refresh_storage(storage_directory: Path) -> None:
    if storage_directory.exists():
        remove_content_recursively_from(storage_directory)
    storage_directory.mkdir(parents=True, exist_ok=True)


def generate_new_filename(storage_directory: Path) -> Path:
    filename = "sales_2022-08-09.json"
    return storage_directory / filename


def store_data(file_path: Path, content: list[dict]) -> None:
    with file_path.open("w", encoding="utf-8") as file:
        dump_json(content, file, ensure_ascii=False, indent=4)


def dump_to_folder(content: list[dict], raw_dir: str = "../storage/raw") -> str:
    storage_path = resolve_path_to(raw_dir)
    refresh_storage(storage_path)
    file_path = generate_new_filename(storage_path)

    store_data(file_path, content)

    return str(file_path)
