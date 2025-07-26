from forecast.forecast_rate import prophet_forecast, ForecastConfig
from tests.conftest import TEST_DATADIR


def test_forecast():
    config = ForecastConfig(data_dir=TEST_DATADIR, plot_dir=TEST_DATADIR)
    prophet_forecast(config)
    assert (TEST_DATADIR / 'prophet_forecats.png').exists()
