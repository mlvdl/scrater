from typing import Tuple
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

from loguru import logger

from scrape_rate.config import DATA_DIR, TIME0


def plot_rates() -> None:
    styles = ['plotly', 'plotly_dark']
    
    now = pd.Timestamp.now()
    now_dt = now + pd.Timedelta(hours=1)
    ranges = {'day': [now - pd.Timedelta(days=1) + pd.Timedelta(hours=9), now_dt], 
              'week': [now - pd.Timedelta(weeks=1), now_dt],
              'month': [now - pd.Timedelta(weeks=4), now_dt],
              '': [pd.Timestamp(TIME0), now_dt],}
    for style in styles:
        for period, range in ranges.items():
            plot_in_style((period, range), style)


def plot_in_style(range, style: str) -> None:
    df, labels_df = get_dataframes()
    
    fig = go.Figure()
    for column in df.columns:
        if column in labels_df['fundName'].tolist():
            fig.add_trace(go.Scatter(x=df.index, y=df[column],
                                     mode='lines+markers',
                                     name=column.split()[0],
                                     text=df[column],
                                     hoverinfo='y'))

            fig.add_annotation(x=df.index[-1], y=df[column].iloc[-1], text=df[column].iloc[-1])
            if range[0] == 'day':
                today = pd.Timestamp('today').normalize()
                today_rows = df[df.index.date == today.date()]
                first_row_today = today_rows.iloc[0] if not today_rows.empty else None
                fig.add_annotation(x=pd.Timestamp(first_row_today.name), y=first_row_today[column], text=first_row_today[column])

    fig.update_layout(
        title='Interest rate over the past ' + range[0],
        xaxis_title='Date',
        yaxis_title='Rate',
        xaxis=dict(
            tickformat='%Y-%m-%d' if range[0] != 'day' else '%H:%M',
            showgrid=True,
            zeroline=False,
        ),
        legend_title='Rates',
        template=style
    )

    fig.update_xaxes(range=range[1])
    fig.update_traces(marker=dict(size=1), hoverlabel=dict(bgcolor="white", font_size=13, font_family="Rockwell"))

    fig_path = DATA_DIR / f"plots/rates_{range[0]}_{style}"
    fig.write_html(fig_path.with_suffix('.html'))
    fig.write_image(fig_path.with_suffix('.png'))
    # fig.show()

    logger.info(f"Rates plotted to {fig_path}") 


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
