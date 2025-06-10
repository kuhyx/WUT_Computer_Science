@echo off
REM filepath: d:\studia\semestr3\psd\projekt\psd_project\stop_all_windows.bat

echo Stopping all Java applications...

REM Stop Transaction Simulator
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq java.exe" /v /fo list ^| findstr /I "transaction-simulator"') do (
    taskkill /PID %%a /F
)

REM Stop Anomaly Detector
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq java.exe" /v /fo list ^| findstr /I "anomaly-detector"') do (
    taskkill /PID %%a /F
)

REM Stop Kafka Consumer Visualizer
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq java.exe" /v /fo list ^| findstr /I "kafka-consumer-visualizer"') do (
    taskkill /PID %%a /F
)

REM Stop Alarm Visualizer
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq java.exe" /v /fo list ^| findstr /I "alarm-visualizer"') do (
    taskkill /PID %%a /F
)

echo Stopping Docker containers...
docker-compose down

echo All applications have been stopped!
pause