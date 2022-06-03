import pathlib
import sys

import pandas as pd
from faker import Faker

ROOT_DIR = pathlib.Path(__file__).parents[1]
DATA_DIR = ROOT_DIR / "data"

faker = Faker("da_DK")

cols = {
    "omraade": "area_id",
    "mdr_aar": "year_month",
    "lovlige_p_pl_kl_12": "legal_parking_12",
    "optalte_pladser_kl_12": "counted_parking_12",
    "lovlige_p_pl_kl_17": "legal_parking_17",
    "optalte_pladser_kl_17": "counted_parking_17",
    "lovlige_p_pl_kl_22": "legal_parking_22",
    "optalte_pladser_kl_22": "counted_parking_22",
}


def add_hour(df: pd.DataFrame):
    """Add an hour column to the DataFrame based on the count_type column"""
    offset = df.count_type.str.split("_", expand=True).iloc[:, -1].astype("Int64")
    return df.assign(hour=offset)


def normalize_date(df: pd.DataFrame, format_str: str = "%Y%m") -> pd.DataFrame:
    """Nicely format the date string to YYYY-MM format"""
    transformed = pd.to_datetime(df["year_month"], format=format_str).dt.strftime("%Y-%m")
    return df.assign(year_month=transformed)


def normalize_name(df: pd.DataFrame, sep="_") -> pd.DataFrame:
    """Normalize the count type names by removing the suffix"""
    transformed = df.count_type.str.split(sep, expand=True).iloc[:, 0]
    return df.assign(count_type=transformed)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """Transform the raw data"""
    return (df.rename(columns=cols)
            .drop_duplicates(["area_id", "year_month"])
            .pipe(normalize_date)
            .melt(id_vars=["area_id", "year_month"], var_name="count_type", value_name="count")
            .pipe(add_hour)
            .pipe(normalize_name)
            )


def create_dim_area(df: pd.DataFrame):
    """Generate a corresponding dim_area from the transformed data"""
    unique_area_id = df.area_id.nunique()

    dim_area = pd.DataFrame({
        "area_id": df.area_id.unique(),
        "city": [faker.city() for _ in range(unique_area_id)],
        "street_name": [faker.dk_street_name() for _ in range(unique_area_id)],
        "postnr": [faker.postcode() for _ in range(unique_area_id)],
        "nr": [faker.building_number() for _ in range(unique_area_id)]
    })
    return dim_area


def create_dim_parking_types(df: pd.DataFrame) -> pd.DataFrame:
    """Generate a corresponding dim_parking_types from the transformed data"""
    dim_parking_types = pd.DataFrame([
        {"type_id": i,
         "name": name}
        for i, name in enumerate(df.count_type.unique())])
    return dim_parking_types


def map_fkt_ids(dim: pd.DataFrame, fkt: pd.DataFrame) -> pd.DataFrame:
    """Replace count type strings with equivalent IDs"""
    dim_mapping = dim.set_index("name").to_dict()["type_id"]
    return fkt.assign(count_type=fkt.count_type.map(dim_mapping))


def main() -> int:
    raw_data = pd.read_csv(DATA_DIR / "parking_counts_cph.csv", usecols=cols.keys())
    fkt_parking = transform(raw_data)
    dim_parking_types = create_dim_parking_types(fkt_parking)
    dim_area = create_dim_area(fkt_parking)
    fkt_parking = map_fkt_ids(dim_parking_types, fkt_parking)

    fkt_parking.to_csv(DATA_DIR / "fkt_parking.csv", index=False)
    dim_parking_types.to_csv(DATA_DIR / "dim_parking_types.csv", index=False)
    dim_area.to_csv(DATA_DIR / "dim_area.csv", index=False)
    return 0


if __name__ == '__main__':
    sys.exit(main())
