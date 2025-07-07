# Windwise

Windwise is a data collection and analysis system designed to evaluate the accuracy of wind forecasts by correlating predicted wind conditions with actual observations. The system continuously gathers both forecast data and real-world measurements, storing them in a time-series database to enable detailed analysis of forecast performance over time.

## Project structure

- `weather/`: All code related to fetching and ingesting weather observations.
- `forecast/`: Code for fetching and processing forecasts.
- `scheduler/`: Code for scheduling periodic jobs (see below).
- `utils/`: Shared utilities (logging, helpers, etc.).
- `main.py`: Entry point, starts the scheduler.
- `config.py`: Centralized configuration (API keys, intervals, etc.).

## Running

1. Create and set permissions for data directory:
   ```bash
   mkdir -p data
   chown -R $USER ./data
   ```

2. Start the containers:
   ```bash
   docker compose up
   ```

3. Get the container ID:
   ```bash
   docker ps
   ```

4. Generate an admin token (save this for later use):
   ```bash
   docker exec -it <CONTAINER_ID> /bin/bash
   influxdb3 create token --admin
   ```

5. Set required environment variables:
   ```bash
   export INFLUXDB_HOST=localhost:8086
   export INFLUXDB_TOKEN=<ADMIN_TOKEN_FROM_STEP_4>
   export WINDWISE_DATABASE=windwise
   ```

6. Start the application:
   ```bash
   poetry run python main.py
   ```