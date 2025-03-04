from pathlib import Path
from typing import Tuple
from loguru import logger
import pandas as pd
import requests


def scrape_api_url(api_url: str) -> dict:
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Failed to retrieve data. Status code: {response.status_code}")
        raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")


def clean_dataframe_rates(df: pd.DataFrame) -> pd.DataFrame:
    df['fundName'] = df['fundName'].apply(lambda x: str(x).replace('<sup> 2)</sup>', '').strip())
    headers = df['fundName'].tolist()
    df['rate'] = df['rate'].apply(lambda x: str(x).replace('*&nbsp;', ''))
    df['rate'] = df['rate'].apply(lambda x: str(x).replace(',', '.'))
    values = df['rate'].tolist()
    df = pd.DataFrame([values], columns=headers)
    df = df.T.drop_duplicates().T
    return df


def clean_fund_name(name: str) -> str:
    if isinstance(name, str):
        return name.replace('<sup> 2)</sup>', '').strip()
    return name


def get_color(value: float) -> str:
    if value > 0:
        return 'green'
    elif value < 0: 
        return 'red'
    else:
        return 'blue'
    

def get_dataframes(data_dir: Path) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(data_dir / 'updated_rates.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    df = merge_df_columns(df=df, col2keep="3,50% NORDEA KREDIT SDRO ANN SDRO 2056", col2drop="3,5 NDA 2056")
    return df


def merge_df_columns(df: pd.DataFrame, col2keep: str, col2drop: str):
    df[col2keep] = df[col2keep].fillna(df[col2drop])
    df = df.drop(columns=[col2drop])
    return df
 

def get_labels(data_dir: Path, loan_period: int = 30, repayment_freedom: str = 'Nej') -> pd.DataFrame:
    labels_df = pd.read_csv(data_dir / 'labels.csv')
    labels_df = labels_df[labels_df['loanPeriodMax'] == loan_period]
    labels_df = labels_df[labels_df['repaymentFreedomMax'] == repayment_freedom]
    labels_df['fundName'] = labels_df['fundName'].apply(clean_fund_name)
    return labels_df 
