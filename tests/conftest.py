from pathlib import Path

import pytest

TEST_DATADIR = Path(__file__).parent / "data"


@pytest.fixture
def data():
    return {
        "data_dir": TEST_DATADIR,
        "rates_filename": TEST_DATADIR / "updated_rates.csv",
        "forecast_file": TEST_DATADIR / "prophet_forecast.png",
    }