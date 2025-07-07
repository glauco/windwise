from apscheduler.schedulers.background import BackgroundScheduler
from observation import weather_fetcher, weather_ingester
from forecast import forecast_fetcher, forecast_ingester
from utils.logger import logger


def collect_observation():
    logger.info("Starting weather observation collection")
    try:
        observation = weather_fetcher.fetch()
        weather_ingester.ingest(observation)
        logger.info("Weather observation collection completed successfully")
    except Exception as e:
        logger.error(f"Error collecting weather observation: {str(e)}")
        raise


def collect_forecast():
    logger.info("Starting weather forecast collection")
    try:
        hourly_data, daily_data = forecast_fetcher.fetch()
        forecast_ingester.ingest(hourly_data, daily_data)
        logger.info("Weather forecast collection completed successfully")
    except Exception as e:
        logger.error(f"Error collecting weather forecast: {str(e)}")
        raise


def start_scheduler():
    logger.info("Initializing background scheduler")
    scheduler = BackgroundScheduler()

    # Run immediately when starting
    logger.info("Running initial data collection")
    collect_observation()
    collect_forecast()

    # Then schedule recurring jobs
    logger.info("Setting up recurring jobs")
    scheduler.add_job(collect_observation, 'interval', minutes=5)
    scheduler.add_job(collect_forecast, 'interval', hours=6)
    scheduler.start()
    logger.info("Scheduler started successfully")
