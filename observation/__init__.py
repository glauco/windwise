import os
from .fetcher import WeatherObservationFetcher
from .ingester import WeatherObservationIngester

# Initialize observation components with environment variables
weather_ingester = WeatherObservationIngester(
    host=os.environ["INFLUXDB_HOST"],
    database=os.environ["WINDWISE_DATABASE"],
    token=os.environ["INFLUXDB_TOKEN"]
)

weather_fetcher = WeatherObservationFetcher()
