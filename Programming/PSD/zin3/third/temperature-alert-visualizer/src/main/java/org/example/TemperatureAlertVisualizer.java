package org.example;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.NumberAxis;
import org.jfree.chart.plot.CategoryPlot;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.data.category.DefaultCategoryDataset;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.swing.*;
import java.awt.*;
import java.time.Duration;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.Collections;
import java.util.Properties;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class TemperatureAlertVisualizer {
    private static final Logger logger = LoggerFactory.getLogger(TemperatureAlertVisualizer.class);
    private static final String TOPIC = "Alarm";
    private static final String BOOTSTRAP_SERVERS = "localhost:9092";
    private static final ObjectMapper objectMapper = new ObjectMapper();
    
    private static final ConcurrentHashMap<String, TemperatureAlert> latestAlerts = new ConcurrentHashMap<>();
    private static final DefaultCategoryDataset dataset = new DefaultCategoryDataset();
    private static final JTextArea alertTextArea = new JTextArea(20, 50);
    private static final DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    
    public static void main(String[] args) {
        // Create and configure UI
        setupUI();
        
        // Start Kafka consumer in a separate thread
        Thread consumerThread = new Thread(() -> consumeAlerts());
        consumerThread.setDaemon(true);
        consumerThread.start();
        
        // Schedule regular UI updates
        ScheduledExecutorService executor = Executors.newSingleThreadScheduledExecutor();
        executor.scheduleAtFixedRate(TemperatureAlertVisualizer::updateUI, 0, 2, TimeUnit.SECONDS);
    }
    
    private static void setupUI() {
        JFrame frame = new JFrame("Temperature Alert Visualizer");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(800, 600);
        
        JPanel mainPanel = new JPanel(new BorderLayout());
        
        // Create chart for temperatures
        JFreeChart chart = ChartFactory.createBarChart(
            "Temperature Anomalies",
            "Thermometer",
            "Temperature (°C)",
            dataset,
            PlotOrientation.VERTICAL,
            true,
            true,
            false
        );
        
        // Customize chart
        CategoryPlot plot = chart.getCategoryPlot();
        NumberAxis rangeAxis = (NumberAxis) plot.getRangeAxis();
        rangeAxis.setRange(-15.0, 5.0);  // Set range for negative temperatures
        
        ChartPanel chartPanel = new ChartPanel(chart);
        chartPanel.setPreferredSize(new Dimension(800, 300));
        
        // Set up text area for alerts
        alertTextArea.setEditable(false);
        JScrollPane scrollPane = new JScrollPane(alertTextArea);
        
        // Add components to main panel
        mainPanel.add(chartPanel, BorderLayout.CENTER);
        mainPanel.add(scrollPane, BorderLayout.SOUTH);
        
        frame.add(mainPanel);
        frame.setVisible(true);
    }
    
    private static void consumeAlerts() {
        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVERS);
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "temperature-alert-visualizer");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        
        try (KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props)) {
            consumer.subscribe(Collections.singletonList(TOPIC));
            
            while (true) {
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
                
                for (ConsumerRecord<String, String> record : records) {
                    try {
                        JsonNode alertJson = objectMapper.readTree(record.value());
                        
                        TemperatureAlert alert = new TemperatureAlert(
                            alertJson.get("thermometerId").asText(),
                            alertJson.get("temperature").asDouble(),
                            alertJson.get("alertTime").asText(),
                            alertJson.get("message").asText()
                        );
                        
                        latestAlerts.put(alert.thermometerId, alert);
                        logger.info("Received alert: " + alert);
                    } catch (Exception e) {
                        logger.error("Error processing alert record", e);
                    }
                }
            }
        }
    }
    
    private static void updateUI() {
        SwingUtilities.invokeLater(() -> {
            // Update chart data
            dataset.clear();
            StringBuilder alertText = new StringBuilder();
            
            for (TemperatureAlert alert : latestAlerts.values()) {
                // Add to chart
                dataset.addValue(alert.temperature, "Temperature", alert.thermometerId);
                
                // Format timestamp
                LocalDateTime dateTime = LocalDateTime.ofInstant(
                    Instant.parse(alert.alertTime), 
                    ZoneId.systemDefault()
                );
                String formattedTime = formatter.format(dateTime);
                
                // Add to text area
                alertText.append(formattedTime)
                         .append(" | ")
                         .append(alert.thermometerId)
                         .append(" | ")
                         .append(String.format("%.2f°C", alert.temperature))
                         .append(" | ")
                         .append(alert.message)
                         .append("\n");
            }
            
            alertTextArea.setText(alertText.toString());
        });
    }
    
    static class TemperatureAlert {
        String thermometerId;
        double temperature;
        String alertTime;
        String message;
        
        public TemperatureAlert(String thermometerId, double temperature, String alertTime, String message) {
            this.thermometerId = thermometerId;
            this.temperature = temperature;
            this.alertTime = alertTime;
            this.message = message;
        }
        
        @Override
        public String toString() {
            return "Alert{" +
                   "thermometerId='" + thermometerId + '\'' +
                   ", temperature=" + temperature +
                   ", alertTime='" + alertTime + '\'' +
                   ", message='" + message + '\'' +
                   '}';
        }
    }
}
