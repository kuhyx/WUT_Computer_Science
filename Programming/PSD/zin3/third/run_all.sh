#!/bin/bash

# Set working directory to script location
cd "$(dirname "$0")"

# Check if Docker daemon is running
if ! docker info &>/dev/null; then
  echo "ERROR: Docker daemon is not running."
  echo "Please start Docker with: 'sudo systemctl start docker'"
  echo "If you want Docker to start automatically at boot: 'sudo systemctl enable docker'"
  echo "To run Docker without sudo, add your user to the docker group: 'sudo usermod -aG docker $USER'"
  echo "Then log out and log back in for the changes to take effect."
  exit 1
fi

echo "Starting Docker containers..."
docker-compose up -d

# Wait for services to start
echo "Waiting for Kafka and Flink to start..."
sleep 10

echo "Building Maven projects..."
cd temperature-generator && mvn -Dorg.slf4j.simpleLogger.defaultLogLevel=WARN clean package && cd ..
cd temperature-anomaly-detector && mvn -Dorg.slf4j.simpleLogger.defaultLogLevel=WARN clean package && cd ..
cd temperature-alert-visualizer && mvn -Dorg.slf4j.simpleLogger.defaultLogLevel=WARN clean package && cd ..

echo "Creating Kafka topics..."
docker exec psd_project-kafka-1 kafka-topics --create --if-not-exists --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic Temperatura
docker exec psd_project-kafka-1 kafka-topics --create --if-not-exists --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic Alarm

echo "Starting all applications..."

# Start temperature anomaly detector - submit to Flink
echo "Starting Temperature Anomaly Detector..."
cd temperature-anomaly-detector
java -jar target/temperature-anomaly-detector-1.0-SNAPSHOT.jar &
ANOMALY_PID=$!
cd ..

# Start Alert Visualizer
echo "Starting Temperature Alert Visualizer..."
cd temperature-alert-visualizer
java -jar target/temperature-alert-visualizer-1.0-SNAPSHOT.jar &
VISUALIZER_PID=$!
cd ..

# Start Temperature Generator last
echo "Starting Temperature Generator..."
cd temperature-generator
java -jar target/temperature-generator-1.0-SNAPSHOT.jar &
GENERATOR_PID=$!
cd ..

echo "All applications are running!"
echo "Press Ctrl+C to stop all applications"

# Function to handle shutdown
function cleanup {
  echo "Shutting down applications..."
  kill $GENERATOR_PID $VISUALIZER_PID $ANOMALY_PID
  echo "Stopping Docker containers..."
  docker-compose down
  echo "All done!"
  exit 0
}

# Catch shutdown signal
trap cleanup SIGINT SIGTERM

# Keep script running
while true; do
  sleep 1
done
