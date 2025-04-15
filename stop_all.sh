#!/bin/bash

echo "Stopping all Java applications..."
pkill -f "java -jar target/transaction-simulator"
pkill -f "java -jar target/anomaly-detector"
pkill -f "java -jar target/kafka-consumer-visualizer"
pkill -f "java -jar target/alarm-visualizer"

echo "Stopping Docker containers..."
docker-compose down

echo "All applications have been stopped!"
