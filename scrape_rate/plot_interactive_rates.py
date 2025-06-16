from datetime import datetime
from loguru import logger
import pandas as pd
import plotly.graph_objects as go

from scrape_rate.config import DATA_DIR, PLOT_DIR
from scrape_rate.plot_interactive_average import plot_average
from scrape_rate.plot_rates import get_dataframes, get_labels
from scrape_rate.utils import get_color


def plot_rates(average: bool) -> None:
    df = get_dataframes(data_dir=DATA_DIR)
    labels_df = get_labels(DATA_DIR, loan_period=[20, 30], repayment_freedom='Nej')
    drop_colums = [column for column in df.columns if column not in labels_df['fundName'].tolist()]
    df.drop(columns=drop_colums, inplace=True)

    rename_dict = dict(zip(labels_df['fundName'], labels_df['name']))
    df.rename(columns=rename_dict, inplace=True)

    plot_interactive_figure(df_data=df, style='plotly')
    if average:
        plot_average(df_data=df, style='plotly')


def plot_interactive_figure(df_data: pd.DataFrame, style: str) -> None:
    
    fig = go.Figure()

    buttons = []

    for i, rate in enumerate(df_data.columns.tolist()):
        latest_timestamp = df_data.index[-1]
        dt_object = datetime.fromisoformat(str(latest_timestamp))
        latest_date = dt_object.date()
        latest_date = latest_date.isoformat()

        df_data.index = pd.to_datetime(df_data.index)
        first_timestamp = df_data.loc[latest_date].iloc[0]
        first_value = first_timestamp[rate]
        color = get_color(value=(df_data[rate].iloc[-1] - first_value))

        fig.add_trace(
            go.Scatter(
                x=df_data.index, 
                name=df_data[rate].iloc[-1],
                y=df_data[rate],
                visible=(i==0),
                line=dict(color=color),
                showlegend=True
                )
            )
        
        args = [False] * len(df_data.columns)
        args[i] = True
        button = dict(label=rate,
                      method="update",
                      args=[{"visible": args}])
        buttons.append(button)

    fig.update_layout(
        updatemenus=[
            dict(
            type="dropdown",
            direction="down",
            x=1,
            y=1,
            buttons=buttons)
        ],
        barmode="stack",

        title='Interest Rate over Time',
        xaxis_title='Date',
        yaxis_title='Rate',
        xaxis=dict(
            tickformat='%Y-%m-%d',
            showgrid=True,
            zeroline=False,
        ),
        legend_title='Rates',
        template=style
    )
    fig_path = PLOT_DIR / "interactive_rates"
    fig.write_html(fig_path.with_suffix('.html'))
    logger.info(f"Rates plotted to {fig_path}") 
    fig.show()
