from loguru import logger
import pandas as pd
import plotly.graph_objects as go

from scrape_rate.config import DATA_DIR, PLOT_DIR
from scrape_rate.plot_rates import get_dataframes, get_labels


def plot_rates() -> None:
    df = get_dataframes(data_dir=DATA_DIR)
    labels_df = get_labels(DATA_DIR, loan_period=30, repayment_freedom='Nej')
    plot_interactive_figure(df_data=df, df_labels=labels_df, style='plotly')


def plot_interactive_figure(df_data: pd.DataFrame, df_labels: pd.DataFrame, style: str) -> None:
    
    fig = go.Figure()

    buttons = []
    rates = df_labels['fundName'].tolist()
    
    for i, column in enumerate(rates):
        fig.add_trace(
            go.Scatter(
                x=df_data.index, 
                name=column,
                y=df_data[column],
                visible=(i==0)
                )
            )
        
        args = [False] * len(df_data.columns)
        args[i] = True
        button = dict(label = column,
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
