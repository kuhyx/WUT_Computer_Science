#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

PROJECT_ROOT=$(pwd)
TOPICS=("transactions" "alerts")

function check_prerequisites {
    echo -e "${BLUE}Checking prerequisites...${NC}"
    
    # Check for Java
    if ! command -v java &> /dev/null; then
        echo -e "${RED}Java is not installed. Please install JDK 11 or higher.${NC}"
        exit 1
    fi
    
    # Check for Maven
    if ! command -v mvn &> /dev/null; then
        echo -e "${RED}Maven is not installed. Please install Maven.${NC}"
        exit 1
    fi
    
    # Check for Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Docker is not installed. Please install Docker.${NC}"
        exit 1
    fi
    
    # Check for docker-compose
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}Docker Compose is not installed. Please install Docker Compose.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}All prerequisites are met.${NC}"
}

function build_projects {
    echo -e "${BLUE}Building all projects...${NC}"
    
    # Build each project
    for project in "transaction-simulator" "kafka-consumer-visualizer" "anomaly-detector" "alarm-visualizer"; do
        echo -e "${YELLOW}Building $project...${NC}"
        cd "$PROJECT_ROOT/$project"
        mvn clean package -DskipTests
        
        if [ $? -ne 0 ]; then
            echo -e "${RED}Failed to build $project.${NC}"
            exit 1
        fi
    done
    
    cd "$PROJECT_ROOT"
    echo -e "${GREEN}All projects built successfully.${NC}"
}

function start_infrastructure {
    echo -e "${BLUE}Starting Kafka and Flink containers...${NC}"
    
    docker-compose up -d
    
    # Wait for Kafka to be ready
    echo -e "${YELLOW}Waiting for Kafka to be ready...${NC}"
    sleep 10
    
    # Create Kafka topics
    for topic in "${TOPICS[@]}"; do
        echo -e "${YELLOW}Creating Kafka topic: $topic${NC}"
        docker-compose exec kafka kafka-topics --create \
            --topic "$topic" \
            --bootstrap-server localhost:9092 \
            --partitions 3 \
            --replication-factor 1 \
            --if-not-exists
    done
    
    echo -e "${GREEN}Infrastructure is up and running.${NC}"
}

function start_applications {
    echo -e "${BLUE}Starting applications...${NC}"
    
    # Start anomaly detector (Flink app)
    echo -e "${YELLOW}Starting Anomaly Detector (Flink App)...${NC}"
    cd "$PROJECT_ROOT/anomaly-detector"
    java -jar target/anomaly-detector-1.0-SNAPSHOT.jar > "$PROJECT_ROOT/logs/anomaly-detector.log" 2>&1 &
    ANOMALY_DETECTOR_PID=$!
    echo $ANOMALY_DETECTOR_PID > "$PROJECT_ROOT/logs/anomaly-detector.pid"
    
    sleep 5
    
    # Start alarm visualizer
    echo -e "${YELLOW}Starting Alarm Visualizer...${NC}"
    cd "$PROJECT_ROOT/alarm-visualizer"
    java -jar target/alarm-visualizer-1.0-SNAPSHOT.jar > "$PROJECT_ROOT/logs/alarm-visualizer.log" 2>&1 &
    ALARM_VISUALIZER_PID=$!
    echo $ALARM_VISUALIZER_PID > "$PROJECT_ROOT/logs/alarm-visualizer.pid"
    
    # Start test consumer/visualizer
    echo -e "${YELLOW}Starting Test Consumer Visualizer...${NC}"
    cd "$PROJECT_ROOT/kafka-consumer-visualizer"
    java -jar target/kafka-consumer-visualizer-1.0-SNAPSHOT.jar > "$PROJECT_ROOT/logs/consumer-visualizer.log" 2>&1 &
    CONSUMER_PID=$!
    echo $CONSUMER_PID > "$PROJECT_ROOT/logs/consumer-visualizer.pid"
    
    sleep 5
    
    # Start transaction simulator
    echo -e "${YELLOW}Starting Transaction Simulator...${NC}"
    cd "$PROJECT_ROOT/transaction-simulator"
    java -jar target/transaction-simulator-1.0-SNAPSHOT.jar > "$PROJECT_ROOT/logs/transaction-simulator.log" 2>&1 &
    SIMULATOR_PID=$!
    echo $SIMULATOR_PID > "$PROJECT_ROOT/logs/transaction-simulator.pid"
    
    cd "$PROJECT_ROOT"
    echo -e "${GREEN}All applications are running.${NC}"
    echo -e "${GREEN}Log files are available in the logs directory.${NC}"
}

function stop_applications {
    echo -e "${BLUE}Stopping applications...${NC}"
    
    # Stop all Java applications
    if [ -f "$PROJECT_ROOT/logs/transaction-simulator.pid" ]; then
        kill $(cat "$PROJECT_ROOT/logs/transaction-simulator.pid") 2>/dev/null
        rm "$PROJECT_ROOT/logs/transaction-simulator.pid"
    fi
    
    if [ -f "$PROJECT_ROOT/logs/consumer-visualizer.pid" ]; then
        kill $(cat "$PROJECT_ROOT/logs/consumer-visualizer.pid") 2>/dev/null
        rm "$PROJECT_ROOT/logs/consumer-visualizer.pid"
    fi
    
    if [ -f "$PROJECT_ROOT/logs/anomaly-detector.pid" ]; then
        kill $(cat "$PROJECT_ROOT/logs/anomaly-detector.pid") 2>/dev/null
        rm "$PROJECT_ROOT/logs/anomaly-detector.pid"
    fi
    
    if [ -f "$PROJECT_ROOT/logs/alarm-visualizer.pid" ]; then
        kill $(cat "$PROJECT_ROOT/logs/alarm-visualizer.pid") 2>/dev/null
        rm "$PROJECT_ROOT/logs/alarm-visualizer.pid"
    fi
    
    echo -e "${GREEN}All applications stopped.${NC}"
}

function stop_infrastructure {
    echo -e "${BLUE}Stopping infrastructure...${NC}"
    
    docker-compose down
    
    echo -e "${GREEN}Infrastructure stopped.${NC}"
}

function show_logs {
    echo -e "${BLUE}Available logs:${NC}"
    ls -l "$PROJECT_ROOT/logs"
    
    echo -e "${YELLOW}Use 'tail -f logs/[filename]' to view a specific log.${NC}"
}

function print_usage {
    echo -e "${BLUE}Credit Card Transaction Anomaly Detection System${NC}"
    echo -e "Usage: $0 [options]"
    echo -e "Options:"
    echo -e "  ${GREEN}start${NC}       Build and start the entire system"
    echo -e "  ${GREEN}stop${NC}        Stop all components"
    echo -e "  ${GREEN}restart${NC}     Restart the entire system"
    echo -e "  ${GREEN}status${NC}      Check if components are running"
    echo -e "  ${GREEN}logs${NC}        Show log files"
}

function check_status {
    echo -e "${BLUE}Checking system status...${NC}"
    
    # Check Docker containers
    echo -e "${YELLOW}Docker containers:${NC}"
    docker-compose ps
    
    # Check Java processes
    echo -e "\n${YELLOW}Java applications:${NC}"
    for app in "transaction-simulator" "consumer-visualizer" "anomaly-detector" "alarm-visualizer"; do
        if [ -f "$PROJECT_ROOT/logs/$app.pid" ]; then
            pid=$(cat "$PROJECT_ROOT/logs/$app.pid")
            if ps -p $pid > /dev/null; then
                echo -e "${GREEN}$app is running (PID: $pid)${NC}"
            else
                echo -e "${RED}$app is not running (stale PID file)${NC}"
            fi
        else
            echo -e "${RED}$app is not running${NC}"
        fi
    done
}

# Create logs directory
mkdir -p "$PROJECT_ROOT/logs"

# Parse command-line arguments
case "$1" in
    start)
        check_prerequisites
        build_projects
        start_infrastructure
        start_applications
        ;;
    stop)
        stop_applications
        stop_infrastructure
        ;;
    restart)
        stop_applications
        stop_infrastructure
        sleep 5
        start_infrastructure
        sleep 5
        start_applications
        ;;
    status)
        check_status
        ;;
    logs)
        show_logs
        ;;
    *)
        print_usage
        ;;
esac
