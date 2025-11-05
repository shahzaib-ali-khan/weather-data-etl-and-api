import os
from pathlib import Path
from typing import Optional

import pandas as pd
import structlog

from .api_client import DWDClient

logger = structlog.get_logger()


def ensure_directory_exists(directory: Path) -> None:
    directory.mkdir(parents=True, exist_ok=True)


def download_files(saving_dir: Path, links: list[str], overwrite: bool = False) -> None:
    """
    Downloads files from provided URLs into saving_dir.
    Skips files that already exist unless overwrite=True.
    """

    ensure_directory_exists(saving_dir)
    api_client = DWDClient()

    for url in links:
        filename = url.split("/")[-1]

        # --- Skip if file already exists ---
        if (saving_dir / filename).exists() and not overwrite:
            logger.info(f"Skipping {filename} (already exists)")
            continue

        logger.info(f"Downloading {filename}...")

        response_content = api_client.get_response_content(url=url, method="get")

        with open(os.path.join(saving_dir, filename), "wb") as f:
            f.write(response_content)


def extract_station_id_from_second_row(csv_file: Path) -> Optional[str]:
    """
    Extract station ID from the second row of the CSV.
    DWD files often have: 'Stations_id:12345' in one of the columns.
    """

    station_id = None
    try:
        # Read only first 0th column
        df_preview = pd.read_csv(
            csv_file, sep=";", encoding="latin1", nrows=2, header=None, usecols=[0]
        )
        station_id = df_preview.iloc[1, 0].strip()

        if station_id:
            return station_id
        else:
            logger.warning(f"Could not extract station_id from {csv_file.name} ")
            return None
    except Exception as e:
        logger.error(f"Failed to extract station_id from {csv_file.name}: {e}")

        return station_id


def filter_dataframe_columns(df: pd.DataFrame) -> pd.DataFrame:
    # Step 1: Define desired columns (exact names!)
    desired_cols = ["station_id", "source_file", "datetime", "Temperatur (2m)"]

    cols_to_keep = [col for col in desired_cols if col in df.columns]

    filtered_df = df[cols_to_keep]

    return filtered_df


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    name_cols_mapping = {"Temperatur (2m)": "temprature"}

    renamed_df = df.rename(columns=name_cols_mapping, inplace=False)

    return renamed_df


def clean_column(df: pd.DataFrame) -> pd.DataFrame:
    cols = ["temprature"]

    for col in cols:
        df[col] = df[col].astype(str).str.replace(",", ".")

        df[col] = df[col].str.replace('"', "").str.strip()

        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def calculate_stats(df: pd.DataFrame) -> pd.DataFrame:
    df["average"] = df["temprature"].mean()
    df["min"] = df["temprature"].min()
    df["max"] = df["temprature"].max()

    return df
