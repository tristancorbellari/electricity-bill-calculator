import calendar
import json
import pandas as pd


@staticmethod
def get_data_from_files(load_profile_filename, block_tariff_filename):
    """Retrieves data from the specified load profile and block tariff format"""

    load_profile_data = pd.read_csv(load_profile_filename)

    load_profile_data["forwardActiveEnergy Value"] = (
        load_profile_data["forwardActiveEnergy Value"] / 1000.0
    )  # Convert watt-hours to kilowatt-hours

    # Determine all calendar months which are present in the load profile
    load_profile_data["Time of Reading - Local"] = pd.to_datetime(
        load_profile_data["Time of Reading - Local"]
    )
    months_grouped = load_profile_data.groupby(
        load_profile_data["Time of Reading - Local"].dt.month
    )
    calendar_months = [
        calendar.month_name[month] for month in months_grouped.indices.keys()
    ]

    f = open(block_tariff_filename)
    block_tariff_json = json.load(f)
    f.close()

    # Get the boundaries and costs for each block tariff
    block_tariff_data = [
        [block["start"] for block in block_tariff_json["tariff_blocks"]],
        [block["cost"] for block in block_tariff_json["tariff_blocks"]],
    ]

    return load_profile_data, block_tariff_data, calendar_months
