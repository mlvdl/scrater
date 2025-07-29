import arrow
import pandas as pd
from loguru import logger

from scrater.config import DATA_DIR, T0
from utils import clean_dataframe_rates


def get_initial_rates():

    df = pd.read_csv(DATA_DIR / 'labels.csv')
    df = clean_dataframe_rates(df)
    df['timestamp'] = arrow.get(T0)
    df = df.set_index('timestamp')

    df.to_csv(DATA_DIR / 'rates.csv')
    logger.debug(f"Initial rates: \n{df}")


get_initial_rates()
