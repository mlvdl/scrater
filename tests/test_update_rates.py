from config import DATA_DIR, THRESHOLD
from scrater.scrape.update_rates import update_rates
from scrater.utils import count_lines
from utils import get_dataframe


def test_update_rates(data):
    initial_lines = count_lines(data["rates_filename"])
    update_rates(data_dir=data["data_dir"])
    final_lines = count_lines(data["rates_filename"])
    assert final_lines == initial_lines + 1


def test_threshold(data):
    df = get_dataframe(DATA_DIR)
    latest_updated_rate = df["3,50% NORDEA KREDIT SDRO ANN SDRO 2056"].tolist()[-1]
    assert latest_updated_rate < THRESHOLD
