from pathlib import Path

import arrow
import pandas as pd
from loguru import logger

from scrater.config import API_URL
from scrater.utils import scrape_api_url, clean_dataframe_rates


def fetch_new_data() -> pd.DataFrame:
    timestamp = arrow.now(tz='Europe/Paris')
    scraped_json_data = scrape_api_url(api_url=API_URL)
    new_row = pd.DataFrame.from_dict(scraped_json_data)
    new_row = clean_dataframe_rates(new_row)
    new_row['timestamp'] = timestamp
    new_row.set_index('timestamp', inplace=True)
    return new_row


def update_rates(data_dir: Path) -> None:

    df = pd.read_csv(data_dir / 'updated_rates.csv', index_col=0)

    new_row = fetch_new_data()
    df = pd.concat([df, new_row], axis=0)

    timestamp = new_row.index[0]
    backup_file = data_dir / f"updated_rates_backup_{timestamp.format('YYYYMMDD_HHmmss')}.csv"
    (data_dir / 'updated_rates.csv').rename(backup_file)
    df.to_csv(data_dir / 'updated_rates.csv')
    backup_file.unlink()

    logger.debug(f"Updated rates:\n {df}")
    logger.info(f"Updated rates on {timestamp} printed to {data_dir / 'updated_rates.csv'}")
