from pydantic import BaseModel


class WeatherObservation(BaseModel):
    """Weather observation data model containing meteorological measurements."""
    temperature: float
    wind_dir: str
    pressure: float
    humidity: float
    wind_speed: float
