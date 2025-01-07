from typing import Tuple
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from loguru import logger

from scrape_rate.config import DATA_DIR


def plot_rates() -> None:

    df, labels_df = get_dataframes()
    plt.style.use('Solarize_Light2') 
    
    fig = plt.figure(figsize=(10, 7))
    ax = plt.subplot(111)
    for column in df.columns:
        if column in labels_df['fundName'].tolist():
            ax.plot(df.index, df[column], label=column.split()[0])
            if len(df.index) > 1:
                ax.text(x=df.index[-1] + (df.index[-1] - df.index[0]) / 100, y=df[column].iloc[-1], s=str(df[column].iloc[-1]))
            else:
                ax.text(x=df.index[-1], y=df[column].iloc[-1], s=str(df[column].iloc[-1]))

    ax = plt.gca()
    ax.xaxis.set_major_locator(mdates.DayLocator())  # Set major ticks to one per day
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    plt.title('Interest rate over time', fontsize=16)
    plt.ylabel('Rate', fontsize=14)
    plt.legend(title='Rates', fontsize=12)

    plt.xlim(df.index[0] - (df.index[-1] - df.index[0]) / 100, df.index[-1] + (df.index[-1] - df.index[0]) / 10)
    plt.xticks(rotation=45)

    # box = ax.get_position()
    # ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])
    # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.legend(loc='best')

    plt.savefig(DATA_DIR / "rates.png")
    plt.close()
    # plt.show()

    logger.info(f"Rates plotted to {DATA_DIR / 'rates.png'}") 


def get_dataframes() -> Tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(DATA_DIR / 'updated_rates.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    labels_df = pd.read_csv(DATA_DIR / "labels.csv")
    labels_df = labels_df[labels_df['loanPeriodMax'] == 30]
    labels_df = labels_df[labels_df['repaymentFreedomMax'] == 'Nej']
    labels_df['fundName'] = labels_df['fundName'].apply(clean_fund_name)
    return df,labels_df  


def clean_fund_name(name: str) -> str:
    if isinstance(name, str):
        return name.replace('<sup> 2)</sup>', '').strip()
    return name
