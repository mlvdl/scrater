from scrape_rate.plot_interactive_average import plot_average_rates
from scrape_rate.plot_interactive_rates import plot_rates
from scrape_rate.update_rates import update_rates


def main(average: bool = False) -> None:
    update_rates()
    plot_rates()
    plot_average_rates()


if __name__ == '__main__':
    main()

