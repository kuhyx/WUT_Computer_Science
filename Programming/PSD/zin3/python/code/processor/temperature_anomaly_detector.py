import os
import json
import sys
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.connectors import FlinkKafkaConsumer, FlinkKafkaProducer
from pyflink.common.time import Time
from pyflink.common.typeinfo import Types
from pyflink.common.watermark_strategy import WatermarkStrategy
from pyflink.datastream.functions import MapFunction, KeyedProcessFunction
from pyflink.datastream.state import ValueStateDescriptor

# Add parent directory to path to import model
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class ReadingMapFunction(MapFunction):
    def map(self, value):
        data = json.loads(value)
        return (data["thermometerId"], data["timestamp"], data["temperature"])

class AnomalyDetectionFunction(KeyedProcessFunction):
    def __init__(self):
        self.window_size = 10 * 1000  # 10 seconds in milliseconds

    def process_element(self, value, ctx):
        thermometer_id, timestamp, temperature = value
        
        # Check if temperature is below zero (anomaly)
        if temperature < 0.0:
            # Create alarm
            alarm = {
                "thermometerId": thermometer_id,
                "timestamp": timestamp,
                "temperature": temperature
            }
            yield json.dumps(alarm)

def add_kafka_dependencies(env):
    """Add Kafka connector dependencies to the environment"""
    
    # User-specific paths where JAR files are located
    kafka_path = "/home/psd/Downloads/kafka_2.13-3.4.0/libs"
    flink_path = "/home/psd/Downloads/flink-1.17.0/lib"
    
    # Required JAR files
    kafka_jars = {
        "kafka-clients": "kafka-clients-3.4.0.jar",
        "flink-connector-kafka": None  # Will be detected or reported as missing
    }
    
    jar_paths = []
    
    # Add kafka-clients JAR
    clients_jar = os.path.join(kafka_path, kafka_jars["kafka-clients"])
    if os.path.exists(clients_jar):
        jar_paths.append(f"file://{clients_jar}")
    else:
        print(f"Warning: Could not find Kafka clients JAR at {clients_jar}")
    
    # Try to find Flink Kafka connector JAR
    connector_found = False
    for file in os.listdir(flink_path):
        if file.startswith("flink-connector-kafka"):
            kafka_jars["flink-connector-kafka"] = file
            jar_paths.append(f"file://{os.path.join(flink_path, file)}")
            connector_found = True
            break
    
    if not connector_found:
        print("Warning: No Flink Kafka connector JAR found! You need to download it.")
        print("You can download it from Maven Central or the Apache Flink website.")
        print("The JAR should be named like 'flink-connector-kafka-1.17.0.jar'")
        print(f"Place it in: {flink_path}")
    
    if jar_paths:
        env.get_config().get_configuration().set_string("pipeline.jars", ";".join(jar_paths))
        print(f"Added JAR files: {jar_paths}")

def main():
    # Create execution environment
    env = StreamExecutionEnvironment.get_execution_environment()
    
    # Add Kafka connector dependencies
    add_kafka_dependencies(env)
    
    # Configure Kafka consumer
    consumer_props = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'temperature-anomaly-detector'
    }
    
    # Create Kafka consumer
    consumer = FlinkKafkaConsumer(
        topics=['Temperatura'],
        deserialization_schema=SimpleStringSchema(),
        properties=consumer_props
    )
    
    # Configure Kafka producer
    producer_props = {
        'bootstrap.servers': 'localhost:9092'
    }
    
    # Create Kafka producer
    producer = FlinkKafkaProducer(
        topic='Alarm',
        serialization_schema=SimpleStringSchema(),
        producer_config=producer_props
    )
    
    # Add source and transformations
    env.add_source(consumer) \
        .map(ReadingMapFunction(), output_type=Types.TUPLE([Types.STRING(), Types.LONG(), Types.DOUBLE()])) \
        .assign_timestamps_and_watermarks(
            WatermarkStrategy.for_monotonous_timestamps()
            .with_timestamp_assigner(lambda event, timestamp: event[1])
        ) \
        .key_by(lambda x: x[0]) \
        .process(AnomalyDetectionFunction()) \
        .add_sink(producer)
    
    # Print the execution plan
    print(env.get_execution_plan())
    
    # Execute
    env.execute("Temperature Anomaly Detector with Time Windows")

if __name__ == "__main__":
    main()
