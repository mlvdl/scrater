from loguru import logger
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt

from scrape_rate.config import COLORS, DATA_DIR, PLOT_DIR
from scrape_rate.plot_rates import get_dataframes, get_labels


def plot_average_rates() -> None:
    df = get_dataframes(data_dir=DATA_DIR)
    labels_df = get_labels(DATA_DIR, loan_period=30, repayment_freedom='Nej')    
    plot_interactive_figure(df_data=df, df_labels=labels_df, style='plotly')


def plot_interactive_figure(df_data: pd.DataFrame, df_labels: pd.DataFrame, style: str) -> None:

    df_data["time_seconds"] = df_data.index.hour * 3600 + df_data.index.minute * 60
    bin_size = 1800
    df_data["time_bin"] = (df_data["time_seconds"] // bin_size) * bin_size

    fig = go.Figure()
    buttons = []
    rates = sorted(df_labels['fundName'].tolist())
    for i, rate in enumerate(rates):
        color = COLORS[i]
        daily_pattern = df_data.groupby("time_bin")[rate].agg(["mean", "std"])
        daily_pattern.fillna(0, inplace=True)
        fig.add_trace(
            go.Scatter(
                x=daily_pattern.index / 3600, 
                name="mean",
                y=daily_pattern["mean"],
                mode='lines',
                line=dict(color=color),
                visible=(i==0)
                )
            )
        fig.add_trace(
            go.Scatter(
                x=daily_pattern.index / 3600, 
                name="±1 Std Dev",
                y=daily_pattern["mean"] - daily_pattern["std"],
                mode='lines',
                line=dict(color=color, dash='dash'),
                visible=(i==0), 
                showlegend=True,
                )
            )
        fig.add_trace(
            go.Scatter(
                x=daily_pattern.index / 3600, 
                name=rate,
                y=daily_pattern["mean"] + daily_pattern["std"],
                mode='lines',
                line=dict(color=color, dash='dash'),
                visible=(i==0),
                showlegend=False
                )
            )
        args = [False] * 3 * len(rates)
        for j in range(3):
            args[3*i+j] = True
        button = dict(label = rate,
                      method = "update",
                      args=[{"visible": args}])
        buttons.append(button)

    fig.update_layout(
        updatemenus=[
            dict(
            type="dropdown",
            direction="down",
            x = 1,
            y = 1,
            buttons = buttons)
        ],
        barmode = "stack",

        title="Average Daily Pattern with Standard Deviation",
        xaxis_title="Time of Day (Hours)", yaxis_title="Rate",
        xaxis=dict(tickmode="array", tickvals=np.arange(0, 25, 2)), 
        legend_title='Rates',
        template=style
    )

    fig_path = PLOT_DIR / "interactive_average_rates"
    fig.write_html(fig_path.with_suffix('.html'))
    logger.info(f"Rates plotted to {fig_path}") 
    fig.show()
