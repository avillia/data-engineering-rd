from json import load as read_from_json
from pathlib import Path


def locate_raw_directory_inside(file_storage: str, sub_directory: str) -> Path:
    raw_path = Path(file_storage) / "raw" / sub_directory
    if not raw_path.exists():
        raise FileNotFoundError(
            f"'raw' '{sub_directory}' directory not found at: {raw_path}"
        )
    return raw_path


def retrieve_data_from(raw_dir_path: Path) -> list[Path]:
    return list(raw_dir_path.iterdir())


def obtain_contents_from(directory: Path) -> list[dict]:
    json_file = next(directory.iterdir())
    with open(json_file, "r", encoding="utf-8") as file:
        return read_from_json(file)


def convert_to_plain_date(directory: Path) -> str:
    return directory.name


def read_raw_files_from(file_storage: str, subdirectory: str) -> dict[str, list[dict]]:
    raw_dir_path = locate_raw_directory_inside(file_storage, subdirectory)
    directory_names = retrieve_data_from(raw_dir_path)

    to_be_converted: dict[str, list[dict]] = {}
    for directory in directory_names:
        file_contents = obtain_contents_from(directory)
        date_as_str = convert_to_plain_date(directory)
        to_be_converted[date_as_str] = file_contents

    return to_be_converted
