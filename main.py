import time
from scheduler.jobs import start_scheduler
from utils.logger import logger

if __name__ == "__main__":
    logger.info("Windwise started")
    start_scheduler()
    try:
        while True:
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutting down...")
