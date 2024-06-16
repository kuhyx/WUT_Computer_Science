#!/bin/bash

# Function to run a script in the background and save its PID
run_script() {
    python $1 &
    echo $!
}

# Function to install Kafka
install_kafka() {
    if ! command -v kafka-server-start &> /dev/null; then
        echo "Kafka is not installed. Installing Kafka..."
        sudo pacman -Syu --noconfirm
        sudo pacman -S --noconfirm kafka
    else
        echo "Kafka is already installed."
    fi
}

# Function to install Flink using yay
install_flink() {
    if ! command -v flink &> /dev/null; then
        echo "Flink is not installed. Installing Flink..."
        if ! command -v yay &> /dev/null; then
            echo "yay is not installed. Installing yay..."
            sudo pacman -S --noconfirm git
            git clone https://aur.archlinux.org/yay.git
            cd yay
            makepkg -si --noconfirm
            cd ..
            rm -rf yay
        fi
        yay -S --noconfirm apache-flink
    else
        echo "Flink is already installed."
    fi
}

# Ensure Kafka and Flink are installed
#install_kafka
#install_flink

# Ensure Kafka and Flink services are running
echo "Starting Kafka and Flink services..."
sudo systemctl start kafka
start-cluster.sh

# Give some time for Kafka and Flink to start
sleep 1

# Start the Kafka producer (Transaction Simulator)
echo "Starting transaction simulator..."
producer_pid=$(run_script './kafka/generate_and_send.py')
echo "Started transaction simulator with PID $producer_pid"

# Give some time for the producer to start and produce initial transactions
sleep 1

# Start the Kafka consumer for testing
echo "Starting Kafka consumer for testing..."
consumer_pid=$(run_script './kafka/kafka_consumer.py')
echo "Started Kafka consumer for testing with PID $consumer_pid"

# Give some time for the consumer to read initial transactions
sleep 1

# Start the Flink job (Anomaly Detector)
echo "Starting Flink anomaly detector..."
flink_pid=$(run_script './flink/anomaly_detector.py')
echo "Started Flink anomaly detector with PID $flink_pid"

# Give some time for the Flink job to start processing
sleep 1

# Start the Flask application (Alarm Reader and Visualizer)
echo "Starting Flask alarm reader..."
flask_pid=$(run_script './webinterface/webinterface.py')
echo "Started Flask alarm reader with PID $flask_pid"

# Function to handle script termination
terminate_scripts() {
    echo "Shutting down..."
    kill $producer_pid
    kill $consumer_pid
    kill $flink_pid
    kill $flask_pid
    echo "All processes terminated."
    # Optionally stop Kafka and Flink services
    sudo systemctl stop kafka
    sudo systemctl stop flink
}

# Trap SIGINT (Ctrl+C) to terminate all subprocesses
trap terminate_scripts SIGINT

# Keep the main script running to allow all subprocesses to continue executing
while true; do
    sleep 1
done
