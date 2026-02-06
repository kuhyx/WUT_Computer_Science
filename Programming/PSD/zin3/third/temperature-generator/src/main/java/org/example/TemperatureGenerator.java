package org.example;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerConfig;
import org.apache.kafka.clients.producer.ProducerRecord;
import org.apache.kafka.common.serialization.StringSerializer;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.Instant;
import java.util.Properties;
import java.util.Random;
import java.util.concurrent.TimeUnit;

public class TemperatureGenerator {
    private static final Logger logger = LoggerFactory.getLogger(TemperatureGenerator.class);
    private static final String TOPIC = "Temperatura";
    private static final String BOOTSTRAP_SERVERS = "localhost:9092";
    private static final int NUM_THERMOMETERS = 5;
    private static final Random random = new Random();
    private static final ObjectMapper objectMapper = new ObjectMapper();

    public static void main(String[] args) {
        // Configure Kafka producer
        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVERS);
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());

        try (KafkaProducer<String, String> producer = new KafkaProducer<>(props)) {
            logger.info("Starting temperature data generation...");
            
            while (true) {
                for (int i = 1; i <= NUM_THERMOMETERS; i++) {
                    // Generate a temperature (sometimes below zero)
                    double temperature = (random.nextDouble() * 40) - 10;  // Range from -10°C to 30°C
                    
                    TemperatureReading reading = new TemperatureReading(
                        "Thermometer-" + i,
                        Instant.now().toString(),
                        temperature
                    );
                    
                    String jsonReading = objectMapper.writeValueAsString(reading);
                    ProducerRecord<String, String> record = new ProducerRecord<>(
                        TOPIC, 
                        reading.thermometerId, 
                        jsonReading
                    );
                    
                    producer.send(record, (metadata, exception) -> {
                        if (exception != null) {
                            logger.error("Error sending temperature data", exception);
                        } else {
                            logger.info("Sent temperature reading: {} | {} | {:.2f}°C", 
                                       reading.thermometerId,
                                       reading.timestamp,
                                       reading.temperature);
                        }
                    });
                }
                
                // Sleep before generating next batch
                TimeUnit.SECONDS.sleep(2);
            }
        } catch (Exception e) {
            logger.error("Error in temperature generator", e);
        }
    }

    public static class TemperatureReading {
        public String thermometerId;
        public String timestamp;
        public double temperature;
        
        public TemperatureReading() {}
        
        public TemperatureReading(String thermometerId, String timestamp, double temperature) {
            this.thermometerId = thermometerId;
            this.timestamp = timestamp;
            this.temperature = temperature;
        }
    }
}
