package processor;

import model.TemperatureAlarm;
import model.TemperatureReading;
import org.apache.flink.api.common.functions.*;
import org.apache.flink.api.java.tuple.Tuple;
import org.apache.flink.api.java.tuple.Tuple3;
import org.apache.flink.streaming.api.TimeCharacteristic;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.timestamps.AscendingTimestampExtractor;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.streaming.connectors.kafka.*;
import org.apache.flink.util.Collector;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.Properties;

public class TemperatureAnomalyDetector {
    public static void main(String[] args) throws Exception {
        // Set up the streaming execution environment
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime);
        
        // Configure Kafka consumer
        Properties consumerProps = new Properties();
        consumerProps.setProperty("bootstrap.servers", "localhost:9092");
        consumerProps.setProperty("group.id", "temperature-anomaly-detector");
        
        // Create Kafka consumer
        FlinkKafkaConsumer<String> consumer = new FlinkKafkaConsumer<>(
            "Temperatura", new SimpleStringSchema(), consumerProps);
            
        // Create Kafka producer for alarms
        Properties producerProps = new Properties();
        producerProps.setProperty("bootstrap.servers", "localhost:9092");
        
        FlinkKafkaProducer<String> producer = new FlinkKafkaProducer<>(
            "Alarm", new SimpleStringSchema(), producerProps);
            
        // Object mapper for JSON conversion
        final ObjectMapper objectMapper = new ObjectMapper();
        
        // Create a DataStream from Kafka
        DataStream<String> inputStream = env.addSource(consumer);
        
        // Parse JSON, assign timestamps, and convert to tuples
        DataStream<Tuple3<String, Long, Double>> temperatureStream = inputStream
            .map(json -> {
                TemperatureReading reading = objectMapper.readValue(json, TemperatureReading.class);
                return new Tuple3<>(reading.getThermometerId(), reading.getTimestamp(), reading.getTemperature());
            })
            .assignTimestampsAndWatermarks(
                new AscendingTimestampExtractor<Tuple3<String, Long, Double>>() {
                    @Override
                    public long extractAscendingTimestamp(Tuple3<String, Long, Double> element) {
                        return element.f1; // timestamp field
                    }
                }
            );
        
        // Group by thermometer ID, apply time window, and detect anomalies
        DataStream<String> alarmStream = temperatureStream
            .keyBy(0) // key by thermometer ID
            .timeWindow(Time.seconds(10)) // 10-second windows
            .apply(new WindowFunction<Tuple3<String, Long, Double>, TemperatureAlarm, Tuple, TimeWindow>() {
                @Override
                public void apply(Tuple key, TimeWindow window, 
                                 Iterable<Tuple3<String, Long, Double>> input, 
                                 Collector<TemperatureAlarm> out) {
                    
                    // Check each reading in the window for below-zero temperature
                    for (Tuple3<String, Long, Double> reading : input) {
                        if (reading.f2 < 0.0) {
                            TemperatureAlarm alarm = new TemperatureAlarm();
                            alarm.setThermometerId(reading.f0);
                            alarm.setTimestamp(reading.f1);
                            alarm.setTemperature(reading.f2);
                            out.collect(alarm);
                        }
                    }
                }
            })
            .map(alarm -> objectMapper.writeValueAsString(alarm));
        
        // Send alarms to Kafka
        alarmStream.addSink(producer);
        
        // Print alarms to console for debugging
        alarmStream.print();
        
        // Execute the Flink job
        env.execute("Temperature Anomaly Detector with Time Windows");
    }
}
