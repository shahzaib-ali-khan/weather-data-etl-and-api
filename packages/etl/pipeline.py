from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin
from zoneinfo import ZoneInfo

import pandas as pd
import structlog
from bs4 import BeautifulSoup

from .api_client import DWDClient
from .database import create_db_engine
from .util import (clean_column, download_files,
                   extract_station_id_from_second_row,
                   filter_dataframe_columns, rename_columns, stats_df)

logger = structlog.get_logger(__name__)


SAVING_DIRECTORY = (
    Path(__file__).parent / "data" / "dwd_csv_files" / datetime.now(tz=ZoneInfo("Europe/Berlin")).strftime("%Y-%m-%d")
)


def extract_data() -> None:
    base_url = "https://opendata.dwd.de/weather/weather_reports/poi/"

    api_client = DWDClient()

    # Step 1: Fetch HTML
    html_data = api_client.get_text_data(url=base_url, method="get")

    # Step 2: Parse HTML
    soup = BeautifulSoup(html_data, "html.parser")

    # Step 3: Find <pre> tag (Apache directory listing)
    pre_tag = soup.find("pre")
    if not pre_tag:
        raise RuntimeError("Could not find <pre> tag in the DWD directory listing")

    # Step 4: Extract all <a> links within it
    links = pre_tag.find_all("a")

    # Step 5: Filter only CSV or CSV.GZ files
    csv_links = [
        urljoin(base_url, link.get("href")) for link in links if link.get("href") and link.get("href").endswith(".csv")
    ]
    logger.info(f"Found {len(csv_links)} CSV files")

    download_files(SAVING_DIRECTORY, csv_links)


def transform_data() -> pd.DataFrame:
    OUTPUT_FILE = SAVING_DIRECTORY / "combined_weather_data.csv"
    all_csv_files = list(SAVING_DIRECTORY.glob("*.csv"))

    if not all_csv_files:
        logger.warning("No CSV files found to transform.")
        return

    dfs = []
    for csv_file in all_csv_files:
        try:
            # --- Step 1: Extract station_id from second row ---
            station_id = extract_station_id_from_second_row(csv_file)

            # --- Step 2: Read actual data, skipping first 2 rows ---
            df = pd.read_csv(
                csv_file,
                sep=";",
                encoding="latin1",
                skiprows=2,  # Skip metadata rows
                on_bad_lines="warn",  # Handle malformed lines gracefully
            )

            if df.empty:
                logger.warning(f"Empty data in {csv_file.name} after skipping rows.")
                continue

            # --- Step 3: Add metadata ---
            df["station_id"] = station_id
            df["source_file"] = csv_file.name

            df["datetime"] = pd.to_datetime(
                df["Datum"] + " " + df["Uhrzeit (UTC)"],
                format="%d.%m.%y %H:%M",
                utc=True,
            )

            dfs.append(df)
            logger.info(f"Loaded {csv_file.name} | {len(df)} rows | station_id: {station_id}")

        except Exception as e:
            logger.error(f"Failed to process {csv_file.name}: {e}", exc_info=True)

    # --- Step 4: Combine all ---
    if not dfs:
        logger.warning("No valid data loaded from any file.")
        exit(1)

    combined_df = pd.concat(dfs, ignore_index=True)
    filtered_dataframe = filter_dataframe_columns(rename_columns(combined_df))
    casted_column_df = clean_column(filtered_dataframe)

    # Drop rows that does not have temperature
    casted_column_df.dropna(subset=["temperature"], inplace=True)

    logger.info(f"Combined {len(dfs)} files into {len(casted_column_df)} rows → {OUTPUT_FILE}")

    return casted_column_df


def load_data(df: pd.DataFrame) -> None:
    db_engine = create_db_engine()

    df.to_sql("weather", con=db_engine, if_exists="append", index=False, chunksize=200)

    statistics_df = stats_df(df)
    statistics_df.to_sql("weather_stats", con=db_engine, if_exists="append", index=False)


def run_pipeline():
    extract_data()
    df = transform_data()
    load_data(df)
