import os
from .fetcher import WeatherForecastFetcher
from .ingester import WeatherForecastIngester

# Initialize forecast components with environment variables
forecast_ingester = WeatherForecastIngester(
    host=os.environ["INFLUXDB_HOST"],
    database=os.environ["WINDWISE_DATABASE"],
    token=os.environ["INFLUXDB_TOKEN"]
)

forecast_fetcher = WeatherForecastFetcher()
