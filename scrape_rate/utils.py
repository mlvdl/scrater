from pathlib import Path
from typing import List, Optional, Tuple
from loguru import logger
import pandas as pd
import requests

from scrape_rate.config import DATA_DIR


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
    logger.debug(f"Value: {value}")
    if value > 0:
        return 'green'
    elif value < 0: 
        return 'red'
    else:
        return 'blue'
    

def get_dataframe(data_dir: Path) -> pd.DataFrame:
    df = pd.read_csv(data_dir / 'updated_rates.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
    df.set_index('timestamp', inplace=True)
    df = merge_df_columns(df=df, col2keep="3,50% NORDEA KREDIT SDRO ANN SDRO 2056", col2drop="3,5 NDA 2056")
    return df


def get_labels(data_dir: Path, loan_period: Optional[List[int]] = None, repayment_freedom: Optional[str] = None) -> pd.DataFrame:
    labels_df = pd.read_csv(data_dir / 'labels.csv')
    
    if loan_period is not None: labels_df = labels_df[labels_df['loanPeriodMax'].isin(loan_period)]
    if repayment_freedom is not None: labels_df = labels_df[labels_df['repaymentFreedomMax'] == repayment_freedom]

    labels_df['fundName'] = labels_df['fundName'].apply(clean_fund_name)
    return labels_df 


def merge_df_columns(df: pd.DataFrame, col2keep: str, col2drop: str):
    df[col2keep] = df[col2keep].fillna(df[col2drop])
    df = df.drop(columns=[col2drop])
    return df
 

def scrape_api_url(api_url: str) -> dict:
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        logger.error(f"Failed to retrieve data. Status code: {response.status_code}")
        raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")


def translate_labels():
    labels = pd.read_csv(DATA_DIR / 'labels.csv')
    names = []
    for row in labels.iterrows():
        name = f"{row[1]['fundName'].split()[0]} - {row[1]['loanPeriodMax']} år"
        names.append(name)
    labels['name'] = names
    labels.to_csv(DATA_DIR / 'labels_translated.csv', index=False)
