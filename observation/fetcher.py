import requests
import re
from .observation import WeatherObservation
import numpy as np
from utils.logger import logger


# API Constants
WEATHER_STATION_URL = (
    "https://www.controlmeteo.com/mkiii/jstags.php?"
    "username=port&passwd=port2020&id=4"
)

# Conversion Constants
METERS_PER_SECOND_TO_KNOTS = 1.8520042801877


class WeatherObservationFetcher:
    """Fetches weather observation data from a remote weather station."""

    def fetch(self) -> WeatherObservation:
        """Fetch and parse current weather observation data.

        Returns:
            WeatherObservation: Parsed weather data

        Raises:
            requests.RequestException: If the HTTP request fails
        """
        logger.info("Starting weather observation data fetch")
        response = requests.get(WEATHER_STATION_URL)
        response.raise_for_status()
        logger.debug("Weather station HTTP request completed successfully")
        observation = self._parse_data(response.text)
        logger.info("Weather observation data fetch completed successfully")
        return observation

    def _extract_var(self, js_code: str, var_name: str) -> str:
        """Extract a variable value from JavaScript code.

        Args:
            js_code: Raw JavaScript code containing variables
            var_name: Name of the variable to extract

        Returns:
            str: Extracted variable value

        Raises:
            ValueError: If variable is not found in the code
        """
        logger.debug(f"Extracting variable '{var_name}' from JavaScript code")
        pattern = fr'var {var_name}\s*=\s*"([^"]+)"'
        match = re.search(pattern, js_code)
        if not match:
            logger.error(f"Failed to extract variable '{var_name}' from JavaScript code")
            raise ValueError(f"Variable {var_name} not found in JavaScript code")
        return match.group(1)

    def _parse_data(self, js_code: str) -> WeatherObservation:
        """Parse weather data from JavaScript code into a WeatherObservation object.

        Args:
            js_code: Raw JavaScript code containing weather data

        Returns:
            WeatherObservation: Parsed weather observation
        """
        logger.debug("Parsing weather observation data from JavaScript code")

        def parse_float(value: str) -> float:
            return float(value.replace(",", "."))

        observation = WeatherObservation(
            temperature=parse_float(self._extract_var(js_code, "temp")),
            wind_dir=self._extract_var(js_code, "dirvelviento"),
            pressure=parse_float(self._extract_var(js_code, "pres")),
            humidity=parse_float(self._extract_var(js_code, "hum")),
            wind_speed=np.round(
                parse_float(
                    self._extract_var(js_code, "velviento")) / METERS_PER_SECOND_TO_KNOTS, 2))
        logger.debug("Weather observation data parsed successfully")
        return observation


if __name__ == "__main__":
    weather_observation = WeatherObservationFetcher().fetch()
    print(weather_observation)
