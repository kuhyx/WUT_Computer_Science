#!/bin/bash

# Directory where the code is located
CODE_DIR="$(dirname "$(readlink -f "$0")")/code"
KAFKA_DIR=${KAFKA_HOME:-"/opt/kafka"}
KAFKA_BIN="$KAFKA_DIR/bin"

# Colors for console output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check if Kafka is running
kafka_running() {
    if command_exists netstat; then
        netstat -tuln | grep -q 9092
    else
        echo -e "${YELLOW}Warning: netstat not available, assuming Kafka is running${NC}"
        return 0
    fi
}

# Cleanup function to kill all processes on exit
cleanup() {
    echo -e "${YELLOW}Shutting down the temperature monitoring system...${NC}"
    
    # Kill all background processes
    if [[ ! -z $GENERATOR_PID ]]; then
        echo "Stopping temperature generator..."
        kill $GENERATOR_PID 2>/dev/null || true
    fi
    
    if [[ ! -z $DETECTOR_PID ]]; then
        echo "Stopping anomaly detector..."
        kill $DETECTOR_PID 2>/dev/null || true
    fi
    
    if [[ ! -z $VISUALIZER_PID ]]; then
        echo "Stopping alarm visualizer..."
        kill $VISUALIZER_PID 2>/dev/null || true
    fi
    
    echo -e "${GREEN}All components stopped successfully.${NC}"
    exit 0
}

# Register the cleanup function for script termination
trap cleanup EXIT INT TERM

# Check Python environment
if ! command_exists python3; then
    echo -e "${RED}Error: Python3 is not installed. Please install Python3 and try again.${NC}"
    exit 1
fi

KAFKA_BIN="/home/psd/Downloads/kafka_2.13-3.4.0/bin"
# Check if Kafka is running
echo "Checking Kafka status..."
if ! kafka_running; then
    echo -e "${YELLOW}Kafka is not running. Attempting to start Kafka...${NC}"
    
    # Check Zookeeper first
    if ! netstat -tuln | grep -q 2181; then
        echo "Starting Zookeeper..."
        if [[ -f "$KAFKA_BIN/zookeeper-server-start.sh" ]]; then
            "$KAFKA_BIN/zookeeper-server-start.sh" "$KAFKA_DIR/config/zookeeper.properties" > /dev/null 2>&1 &
            sleep 5
        else
            echo -e "${RED}Error: Zookeeper startup script not found.${NC}"
            exit 1
        fi
    fi
    
    # Start Kafka
    if [[ -f "$KAFKA_BIN/kafka-server-start.sh" ]]; then
        echo "Starting Kafka server..."
        "$KAFKA_BIN/kafka-server-start.sh" "$KAFKA_DIR/config/server.properties" > /dev/null 2>&1 &
        sleep 10
        
        # Check if Kafka started successfully
        if ! kafka_running; then
            echo -e "${RED}Error: Failed to start Kafka. Please check Kafka installation.${NC}"
            exit 1
        fi
    else
        echo -e "${RED}Error: Kafka startup script not found.${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}Kafka is running.${NC}"

# Create Kafka topics if they don't exist
echo "Creating Kafka topics if they don't exist..."
if [[ -f "$KAFKA_BIN/kafka-topics.sh" ]]; then
    "$KAFKA_BIN/kafka-topics.sh" --create --bootstrap-server localhost:9092 --topic Temperatura --partitions 3 --replication-factor 1 --if-not-exists
    "$KAFKA_BIN/kafka-topics.sh" --create --bootstrap-server localhost:9092 --topic Alarm --partitions 3 --replication-factor 1 --if-not-exists
else
    echo -e "${YELLOW}Warning: Kafka topics script not found. Assuming topics already exist.${NC}"
fi

# Start components in the correct order
echo -e "${GREEN}Starting temperature monitoring system...${NC}"

# 1. Start the alarm visualizer
echo "Starting alarm visualizer..."
python3 "$CODE_DIR/visualizer/alarm_visualizer.py" &
VISUALIZER_PID=$!
sleep 2

# 2. Start the anomaly detector
echo "Starting temperature anomaly detector..."
python3 "$CODE_DIR/processor/temperature_anomaly_detector.py" &
DETECTOR_PID=$!
sleep 2

# 3. Start the temperature generator
echo "Starting temperature generator..."
python3 "$CODE_DIR/generator/temperature_generator.py" &
GENERATOR_PID=$!

echo -e "${GREEN}All components started successfully!${NC}"
echo "Press Ctrl+C to stop the system."

# Wait for any process to exit
wait
