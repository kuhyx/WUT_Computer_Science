package org.example;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.common.functions.FilterFunction;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.api.java.functions.KeySelector;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.connector.kafka.sink.KafkaRecordSerializationSchema;
import org.apache.flink.connector.kafka.sink.KafkaSink;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.Instant;
import java.util.Properties;

public class TemperatureAnomalyDetector {
    private static final Logger logger = LoggerFactory.getLogger(TemperatureAnomalyDetector.class);
    private static final String INPUT_TOPIC = "Temperatura";
    private static final String OUTPUT_TOPIC = "Alarm";
    private static final String BOOTSTRAP_SERVERS = "localhost:9092";
    private static final ObjectMapper objectMapper = new ObjectMapper();

    public static void main(String[] args) throws Exception {
        logger.info("Starting Temperature Anomaly Detector application");
        
        // Create and configure the Flink execution environment
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        
        // Set parallelism to 1 for simplified processing
        env.setParallelism(1);

        logger.info("Configuring Kafka source for topic: {}", INPUT_TOPIC);
        
        // Configure Kafka source
        KafkaSource<String> source = KafkaSource.<String>builder()
                .setBootstrapServers(BOOTSTRAP_SERVERS)
                .setTopics(INPUT_TOPIC)
                .setGroupId("temperature-anomaly-detector")
                .setStartingOffsets(OffsetsInitializer.earliest())
                .setValueOnlyDeserializer(new SimpleStringSchema())
                .build();

        logger.info("Configuring Kafka sink for topic: {}", OUTPUT_TOPIC);
        
        // Configure Kafka sink
        Properties producerProps = new Properties();
        producerProps.setProperty(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVERS);
        
        KafkaSink<String> sink = KafkaSink.<String>builder()
                .setBootstrapServers(BOOTSTRAP_SERVERS)
                .setRecordSerializer(KafkaRecordSerializationSchema.<String>builder()
                        .setTopic(OUTPUT_TOPIC)
                        .setValueSerializationSchema(new SimpleStringSchema())
                        .build())
                .setKafkaProducerConfig(producerProps)
                .build();

        logger.info("Building temperature processing pipeline");
        
        // Parse temperature readings from Kafka
        DataStream<TemperatureReading> temperatureStream = env
                .fromSource(source, WatermarkStrategy.noWatermarks(), "Kafka Source")
                .map(new MapFunction<String, TemperatureReading>() {
                    @Override
                    public TemperatureReading map(String jsonString) throws Exception {
                        logger.debug("Received temperature reading: {}", jsonString);
                        return objectMapper.readValue(jsonString, TemperatureReading.class);
                    }
                });

        // Detect anomalies (temperatures below zero)
        DataStream<String> alarmStream = temperatureStream
                .filter(new FilterFunction<TemperatureReading>() {
                    @Override
                    public boolean filter(TemperatureReading reading) throws Exception {
                        boolean isAnomaly = reading.temperature < 0.0;
                        if (isAnomaly) {
                            logger.info("Anomaly detected: {}°C from {}", 
                                reading.temperature, reading.thermometerId);
                        }
                        return isAnomaly;
                    }
                })
                // Group by thermometer ID
                .keyBy((KeySelector<TemperatureReading, String>) reading -> reading.thermometerId)
                // Apply a time window to aggregate anomalies
                .window(TumblingProcessingTimeWindows.of(Time.seconds(10)))
                .apply(new TemperatureWindowFunction())
                .map(new MapFunction<TemperatureAlert, String>() {
                    @Override
                    public String map(TemperatureAlert alert) throws Exception {
                        ObjectNode alertJson = objectMapper.createObjectNode();
                        alertJson.put("thermometerId", alert.thermometerId);
                        alertJson.put("temperature", alert.temperature);
                        alertJson.put("alertTime", alert.alertTime);
                        alertJson.put("message", alert.message);
                        String json = objectMapper.writeValueAsString(alertJson);
                        logger.info("Producing alert: {}", json);
                        return json;
                    }
                });

        // Send alerts to Kafka
        alarmStream.sinkTo(sink);

        logger.info("Executing Temperature Anomaly Detector job");
        
        // Execute the Flink job
        try {
            env.execute("Temperature Anomaly Detector");
        } catch (Exception e) {
            logger.error("Error executing Flink job", e);
            throw e;
        }
    }

    // POJO classes
    public static class TemperatureReading {
        public String thermometerId;
        public String timestamp;
        public double temperature;
        
        public TemperatureReading() {}
    }
    
    public static class TemperatureAlert {
        public String thermometerId;
        public double temperature;
        public String alertTime;
        public String message;
        
        public TemperatureAlert(String thermometerId, double temperature, String message) {
            this.thermometerId = thermometerId;
            this.temperature = temperature;
            this.alertTime = Instant.now().toString();
            this.message = message;
        }
    }
}
