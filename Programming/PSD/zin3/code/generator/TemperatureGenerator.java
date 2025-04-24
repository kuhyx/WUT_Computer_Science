package generator;

import model.TemperatureReading;
import org.apache.kafka.clients.producer.*;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.Properties;
import java.util.Random;

public class TemperatureGenerator {
    public static void main(String[] args) throws Exception {
        // Set up Kafka producer properties
        Properties props = new Properties();
        props.put("bootstrap.servers", "localhost:9092");
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        
        Producer<String, String> producer = new KafkaProducer<>(props);
        ObjectMapper objectMapper = new ObjectMapper();
        Random random = new Random();
        
        // Generate a fixed number of thermometer IDs
        String[] thermometerIds = {"Therm-1", "Therm-2", "Therm-3", "Therm-4", "Therm-5"};
        
        try {
            while (true) {
                for (String thermometerId : thermometerIds) {
                    // Generate a random temperature between -10 and 30 degrees
                    double temperature = random.nextDouble() * 40 - 10;
                    
                    TemperatureReading reading = new TemperatureReading();
                    reading.setThermometerId(thermometerId);
                    reading.setTimestamp(System.currentTimeMillis());
                    reading.setTemperature(temperature);
                    
                    // Convert to JSON
                    String json = objectMapper.writeValueAsString(reading);
                    
                    // Send to Kafka topic "Temperatura"
                    ProducerRecord<String, String> record = new ProducerRecord<>("Temperatura", thermometerId, json);
                    producer.send(record);
                    
                    System.out.println("Sent: " + json);
                }
                
                // Sleep for a second
                Thread.sleep(1000);
            }
        } finally {
            producer.close();
        }
    }
}
