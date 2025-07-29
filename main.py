from scrater.config import DATA_DIR
from scrater.plot.plot_interactive_rates import plot_rates
from scrater.scrape.update_rates import update_rates


def main(average: bool = True) -> None:
    update_rates(data_dir=DATA_DIR)
    plot_rates(average=average)


if __name__ == '__main__':
    main()

