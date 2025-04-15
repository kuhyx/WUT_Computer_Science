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

# Note about docker-compose.yml
echo "Note: Your docker-compose.yml contains an obsolete 'version' attribute that should be removed."

echo "Starting Docker containers..."
docker-compose up -d

echo "Building Maven projects..."
cd transaction-simulator && mvn -Dorg.slf4j.simpleLogger.defaultLogLevel=WARN clean package && cd ..
cd anomaly-detector && mvn -Dorg.slf4j.simpleLogger.defaultLogLevel=WARN clean package && cd ..
cd kafka-consumer-visualizer && mvn -Dorg.slf4j.simpleLogger.defaultLogLevel=WARN clean package && cd ..
cd alarm-visualizer && mvn -Dorg.slf4j.simpleLogger.defaultLogLevel=WARN clean package && cd ..

echo "Creating Kafka topics..."
docker exec psd_project-kafka-1 kafka-topics --create --if-not-exists --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic transactions
docker exec psd_project-kafka-1 kafka-topics --create --if-not-exists --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic alerts

echo "Starting all applications..."

# Start Flink job (Anomaly Detector)
echo "Starting Anomaly Detector..."
cd anomaly-detector
java -jar target/anomaly-detector-1.0-SNAPSHOT.jar &
ANOMALY_PID=$!
cd ..

# Start Alert Visualizer
echo "Starting Alert Visualizer..."
cd alarm-visualizer
java -jar target/alarm-visualizer-1.0-SNAPSHOT.jar &
ALARM_PID=$!
cd ..

# Start Transaction Consumer/Visualizer
echo "Starting Transaction Consumer..."
cd kafka-consumer-visualizer
java -jar target/kafka-consumer-visualizer-1.0-SNAPSHOT.jar &
CONSUMER_PID=$!
cd ..

# Start Transaction Producer last
echo "Starting Transaction Producer..."
cd transaction-simulator
java -jar target/transaction-simulator-1.0-SNAPSHOT.jar &
PRODUCER_PID=$!
cd ..

echo "All applications are running!"
echo "Press Ctrl+C to stop all applications"

# Function to handle shutdown
function cleanup {
  echo "Shutting down applications..."
  kill $PRODUCER_PID $CONSUMER_PID $ALARM_PID $ANOMALY_PID
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
