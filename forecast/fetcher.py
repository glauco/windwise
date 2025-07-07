import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from utils.logger import logger


# API Constants
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
BARCELONA_LATITUDE = 41.386667
BARCELONA_LONGITUDE = 2.1206
TIMEZONE = "Europe/Berlin"
FORECAST_DAYS = 1
WIND_SPEED_UNIT = "kn"

# Forecast Parameters
DAILY_PARAMS = ["sunrise", "sunset"]
HOURLY_PARAMS = ["temperature_2m", "wind_speed_10m", "wind_gusts_10m", "wind_direction_10m"]
MODEL = "meteofrance_arome_france_hd"

# Cache Settings
CACHE_EXPIRY = 3600
RETRY_ATTEMPTS = 5
RETRY_BACKOFF = 0.2


class WeatherForecastFetcher:
    """Fetches weather forecast data from Open-Meteo API."""

    def __init__(self):
        # Setup the Open-Meteo API client with cache and retry on error
        logger.info("Initializing WeatherForecastFetcher")
        cache_session = requests_cache.CachedSession('.cache', expire_after=CACHE_EXPIRY)
        retry_session = retry(cache_session,
                              retries=RETRY_ATTEMPTS,
                              backoff_factor=RETRY_BACKOFF)
        self.openmeteo = openmeteo_requests.Client(session=retry_session)
        logger.info("WeatherForecastFetcher initialized successfully")

    def fetch(self):
        """Fetches and returns hourly and daily forecast data."""
        logger.info("Starting forecast data fetch")
        response = self._get_forecast_response()
        hourly_dataframe = self._process_hourly_data(response.Hourly())
        daily_dataframe = self._process_daily_data(response.Daily())
        logger.info("Forecast data fetch completed successfully")
        return hourly_dataframe, daily_dataframe

    def _get_forecast_response(self):
        """Makes API request and returns response."""
        logger.debug("Making API request to Open-Meteo")
        params = {
            "latitude": BARCELONA_LATITUDE,
            "longitude": BARCELONA_LONGITUDE,
            "daily": DAILY_PARAMS,
            "hourly": HOURLY_PARAMS,
            "models": MODEL,
            "timezone": TIMEZONE,
            "forecast_days": FORECAST_DAYS,
            "wind_speed_unit": WIND_SPEED_UNIT
        }
        responses = self.openmeteo.weather_api(OPEN_METEO_URL, params=params)
        logger.debug("API request completed successfully")
        return responses[0]

    def _process_hourly_data(self, hourly):
        """Processes hourly forecast data into a DataFrame."""
        logger.debug("Processing hourly forecast data")
        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            ),
            "temperature_2m": hourly.Variables(0).ValuesAsNumpy(),
            "wind_speed_10m": hourly.Variables(1).ValuesAsNumpy(),
            "wind_gusts_10m": hourly.Variables(2).ValuesAsNumpy(),
            "wind_direction_10m": hourly.Variables(3).ValuesAsNumpy()
        }
        return pd.DataFrame(data=hourly_data)

    def _process_daily_data(self, daily):
        """Processes daily forecast data into a DataFrame."""
        logger.debug("Processing daily forecast data")
        daily_data = {
            "date": pd.date_range(
                start=pd.to_datetime(daily.Time(), unit="s", utc=True),
                end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=daily.Interval()),
                inclusive="left"
            ),
            "sunrise": daily.Variables(0).ValuesInt64AsNumpy(),
            "sunset": daily.Variables(1).ValuesInt64AsNumpy()
        }
        return pd.DataFrame(data=daily_data)
