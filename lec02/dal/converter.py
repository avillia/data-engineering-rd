from datetime import datetime


def convert_date_from_iso_to_avro_format(date: str) -> int:
    current_date = datetime.strptime(date, "%Y-%m-%d")
    beginning_of_era = datetime(1970, 1, 1)
    date_difference = current_date - beginning_of_era
    return date_difference.days


def convert_json_to_avro(records: list[dict]) -> list[dict]:
    for record in records:
        record["purchase_date"] = convert_date_from_iso_to_avro_format(
            record["purchase_date"]
        )
    return records
