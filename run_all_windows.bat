@echo off
setlocal enabledelayedexpansion

REM Set working directory to script location
cd /d "%~dp0"
set "PROJECT_ROOT=%cd%"

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker daemon is not running.
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo Starting Docker containers...
docker-compose up -d

echo Creating Kafka topics...
docker exec psd_project-kafka-1 kafka-topics --create --if-not-exists --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic transactions
docker exec psd_project-kafka-1 kafka-topics --create --if-not-exists --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic alerts

echo Starting all applications in new windows...

echo Starting Anomaly Detector...
start "Anomaly Detector" cmd /k "cd /d %PROJECT_ROOT%\anomaly-detector && java --add-opens java.base/java.time=ALL-UNNAMED -jar target\anomaly-detector-1.0-SNAPSHOT.jar"
echo Starting Alert Visualizer...
start "Alert Visualizer" cmd /k "cd /d %PROJECT_ROOT%\alarm-visualizer && java --add-opens java.base/java.time=ALL-UNNAMED -jar target\alarm-visualizer-1.0-SNAPSHOT.jar"
echo Starting Transaction Consumer...
start "Transaction Consumer" cmd /k "cd /d %PROJECT_ROOT%\kafka-consumer-visualizer && java --add-opens java.base/java.time=ALL-UNNAMED -jar target\kafka-consumer-visualizer-1.0-SNAPSHOT.jar"
echo Starting Transaction Producer...
start "Transaction Producer" cmd /k "cd /d %PROJECT_ROOT%\transaction-simulator && java --add-opens java.base/java.time=ALL-UNNAMED -jar target\transaction-simulator-1.0-SNAPSHOT.jar"

echo All applications are running!
echo To stop everything, close all opened windows and run:
echo docker-compose down
pause