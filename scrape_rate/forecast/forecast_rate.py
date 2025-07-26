import dataclasses
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from loguru import logger
from prophet import Prophet

from scrape_rate.utils import get_dataframe, get_labels
from scrape_rate.config import DATA_DIR, PLOT_DIR


@dataclasses.dataclass
class ForecastConfig:
    data_dir: Path = DATA_DIR
    plot_dir: Path = PLOT_DIR
    periods: int = 10
    freq: str = "5min"
    rate: str = "3,50"


def prophet_forecast(config: ForecastConfig):
    data = get_data(config=config)
    logger.debug(data)

    data_resampled = data.resample(config.freq).mean()
    data_resampled.fillna(method='ffill', inplace=True)

    # Prepare the data for Prophet
    data_prophet = data.reset_index()
    data_prophet.columns = ['ds', 'y']

    data_prophet['ds'] = data_prophet['ds'].dt.tz_localize(None)
    data_prophet['ds'] = pd.to_datetime(data_prophet['ds'])
    logger.debug(data_prophet)

    # Fit the Prophet model
    model = Prophet()
    model.fit(data_prophet)

    future = model.make_future_dataframe(periods=config.periods, freq=config.freq)
    forecast = model.predict(future)
    logger.debug(forecast)
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(config.periods))
    model.plot(forecast)
    plt.savefig(config.plot_dir / 'prophet_forcast.png')
    plt.show()


def forecast_rate():
    config = ForecastConfig()
    prophet_forecast(config)


def get_data(config: ForecastConfig):
    df = get_dataframe(data_dir=config.data_dir)
    labels_df = get_labels(config.data_dir, loan_period=[30], repayment_freedom='Nej')
    drop_colums = [column for column in df.columns if column not in labels_df['fundName'].tolist()]
    df.drop(columns=drop_colums, inplace=True)
    drop_colums = [column for column in df.columns if config.rate not in column]
    df.drop(columns=drop_colums, inplace=True)
    rename_dict = dict(zip(labels_df['fundName'], labels_df['name']))
    df.rename(columns=rename_dict, inplace=True)
    df.index = pd.to_datetime(df.index)
    return df


forecast_rate()
