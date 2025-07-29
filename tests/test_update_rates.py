from scrater.scrape.update_rates import update_rates
from scrater.utils import count_lines


def test_update_rates(data):
    initial_lines = count_lines(data["rates_filename"])
    update_rates(data_dir=data["data_dir"])
    final_lines = count_lines(data["rates_filename"])
    assert final_lines == initial_lines + 1
