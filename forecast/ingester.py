from influxdb_client_3 import InfluxDBClient3, Point
import pandas as pd
from utils.logger import logger


class WeatherForecastIngester:
    """Ingests weather forecast data into InfluxDB."""

    def __init__(self, host: str, database: str, token: str):
        logger.info("Initializing WeatherForecastIngester")
        self.client = InfluxDBClient3(
            host=host,
            database=database,
            token=token
        )
        logger.info("WeatherForecastIngester initialized successfully")

    def ingest(self, hourly_data: pd.DataFrame, daily_data: pd.DataFrame) -> None:
        """Ingests hourly and daily forecast data into InfluxDB."""
        logger.info("Starting forecast data ingestion")
        logger.debug("Ingesting hourly forecast data")

        # Convert hourly data to points
        for _, row in hourly_data.iterrows():
            point = Point("weather_forecast_hourly") \
                .time(row['date']) \
                .field("temperature_2m", float(row['temperature_2m'])) \
                .field("wind_speed_10m", float(row['wind_speed_10m'])) \
                .field("wind_gusts_10m", float(row['wind_gusts_10m'])) \
                .field("wind_direction_10m", float(row['wind_direction_10m']))
            self.client.write(record=point)

        logger.debug("Ingesting daily forecast data")
        # Convert daily data to points
        for _, row in daily_data.iterrows():
            point = Point("weather_forecast_daily") \
                .time(row['date']) \
                .field("sunrise", row['sunrise']) \
                .field("sunset", row['sunset'])
            self.client.write(record=point)

        logger.info("Forecast data ingestion completed successfully")
