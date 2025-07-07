from influxdb_client_3 import InfluxDBClient3, Point
from .observation import WeatherObservation
from utils.logger import logger


class WeatherObservationIngester:
    """Pushes weather observations to an InfluxDB 3 instance."""

    def __init__(self, host: str, database: str, token: str):
        logger.info("Initializing WeatherObservationIngester")
        self.client = InfluxDBClient3(
            host=host,
            database=database,
            token=token
        )
        logger.info("WeatherObservationIngester initialized successfully")

    def ingest(self, observation: WeatherObservation) -> None:
        """Ingests a WeatherObservation using line protocol."""
        logger.info("Starting weather observation ingestion")
        logger.debug("Creating observation data point")
        point = Point("weather_observation") \
            .tag("location", "Port Olimpic") \
            .field("temperature", observation.temperature) \
            .field("wind_dir", observation.wind_dir) \
            .field("pressure", observation.pressure) \
            .field("humidity", observation.humidity) \
            .field("wind_speed", observation.wind_speed)

        logger.debug("Writing observation data point to InfluxDB")
        self.client.write(record=point)
        logger.info("Weather observation ingestion completed successfully")
