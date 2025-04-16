from json import load as read_from_json
from pathlib import Path


def locate_raw_directory_inside(file_storage: str, sub_directory: str) -> Path:
    raw_dir_path = Path(file_storage).resolve()
    if not raw_dir_path.exists():
        raise FileNotFoundError(
            f"'raw' '{sub_directory}' directory not found at: {raw_dir_path}"
        )
    return raw_dir_path


def retrieve_data_from(raw_dir_path: Path) -> list[Path]:
    return list(raw_dir_path.iterdir())


def obtain_contents_from(file: Path) -> list[dict]:
    with open(file, "r", encoding="utf-8") as file_contents:
        return read_from_json(file_contents)


def convert_to_plain_date(file: Path) -> str:
    return file.parent.name


def read_raw_files_from(file_storage: str, subdirectory: str) -> dict[str, list[dict]]:
    raw_dir_path = locate_raw_directory_inside(file_storage, subdirectory)
    file_names = retrieve_data_from(raw_dir_path)

    to_be_converted: dict[str, list[dict]] = {}
    for file in file_names:
        date_as_str = convert_to_plain_date(file)
        to_be_converted[date_as_str] = obtain_contents_from(file)

    return to_be_converted
