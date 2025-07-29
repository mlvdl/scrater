from forecast.forecast_rate import prophet_forecast, ForecastConfig
from tests.conftest import TEST_DATADIR


def test_forecast(data):
    config = ForecastConfig(data_dir=TEST_DATADIR, plot_dir=TEST_DATADIR, show=False)
    prophet_forecast(config)
    assert (data["forecast_file"]).exists()
