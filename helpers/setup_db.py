import pathlib

import pandas as pd
import sqlalchemy as sa

ROOT_DIR = pathlib.Path(__file__).parents[1]
DATA_DIR = ROOT_DIR / "data"

engine = sa.create_engine("sqlite:///parking.db")

fkt_parking = pd.read_parquet(DATA_DIR / "fkt_parking.parquet")
dim_area = pd.read_parquet(DATA_DIR / "dim_area.parquet")
dim_parking_types = pd.read_parquet(DATA_DIR / "dim_parking_types.parquet")

fkt_parking.to_sql("fkt_parking", engine, if_exists="replace")
dim_area.to_sql("dim_area", engine, if_exists="replace")
dim_parking_types.to_sql("dim_parking_types", engine, if_exists="replace")
