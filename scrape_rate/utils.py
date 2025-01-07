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
