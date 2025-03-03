from loguru import logger
import plotly.graph_objects as go
from scrape_rate.config import DATA_DIR
from scrape_rate.plot_rates import get_dataframes, get_labels


def plot_rates() -> None:
    plot_in_style(style='plotly')


def plot_in_style(style: str) -> None:
    df = get_dataframes(data_dir=DATA_DIR)
    labels_df = get_labels(DATA_DIR, loan_period=30, repayment_freedom='Nej')
    
    fig = go.Figure()

    buttons = []
    i = 0
    for column in df.columns:
        if column in labels_df['fundName'].tolist():
            fig.add_trace(
                go.Scatter(
                    x=df.index, 
                    name=column,
                    y=df[column],
                    visible=(i==0)
                    )
                )
            
            args = [False] * len(df.columns)
            args[i] = True

            button = dict(label = column,
                          method = "update",
                          args=[{"visible": args}])

            buttons.append(button)
            i+=1

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

    fig_path = DATA_DIR / f"plots/interactive_rates"
    fig.write_html(fig_path.with_suffix('.html'))
    logger.info(f"Rates plotted to {fig_path}") 
    fig.show()
