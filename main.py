from scrape_rate.plot_interactive_rates import plot_rates
from scrape_rate.update_rates import update_rates


def main(average: bool = True) -> None:
    update_rates()
    plot_rates(average=average)


if __name__ == '__main__':
    main()

