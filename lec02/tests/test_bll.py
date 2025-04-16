from pathlib import Path
from shutil import rmtree as remove_content_recursively_from

from assertpy import assert_that

from lec02.bll.loader import convert_data_to_stg_format


def test_no_raw_files_found_to_convert():
    temporary_storage = Path("../test_storage").resolve()
    dated_stg_directory = temporary_storage / "raw" / "test" / "2022-09-09"
    dated_stg_directory.mkdir(parents=True)

    assert_that(convert_data_to_stg_format).raises(FileNotFoundError).when_called_with("/test_storage/raw/test/2022-09-09", "/we/do/not/care/about/this/one")

    remove_content_recursively_from(temporary_storage)
