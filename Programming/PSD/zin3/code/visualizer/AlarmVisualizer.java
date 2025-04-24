package visualizer;

import model.TemperatureAlarm;
import org.apache.kafka.clients.consumer.*;
import javax.swing.*;
import java.awt.*;
import java.time.Duration;
import java.text.SimpleDateFormat;
import java.util.*;
import com.fasterxml.jackson.databind.ObjectMapper;

public class AlarmVisualizer {
    private static DefaultListModel<String> listModel = new DefaultListModel<>();
    private static final int MAX_ALARMS = 100;
    
    public static void main(String[] args) {
        // Set up the GUI
        JFrame frame = new JFrame("Temperature Alarm Visualizer");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(600, 400);
        
        JList<String> alarmList = new JList<>(listModel);
        alarmList.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 12));
        
        JScrollPane scrollPane = new JScrollPane(alarmList);
        frame.getContentPane().add(scrollPane, BorderLayout.CENTER);
        
        JPanel statsPanel = new JPanel();
        JLabel statsLabel = new JLabel("No alarms yet");
        statsPanel.add(statsLabel);
        frame.getContentPane().add(statsPanel, BorderLayout.SOUTH);
        
        frame.setVisible(true);
        
        // Set up Kafka consumer in a separate thread
        Thread consumerThread = new Thread(() -> {
            // Set up Kafka consumer properties
            Properties props = new Properties();
            props.put("bootstrap.servers", "localhost:9092");
            props.put("group.id", "alarm-visualizer");
            props.put("key.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
            props.put("value.deserializer", "org.apache.kafka.common.serialization.StringDeserializer");
            props.put("auto.offset.reset", "latest");
            
            Consumer<String, String> consumer = new KafkaConsumer<>(props);
            consumer.subscribe(Collections.singletonList("Alarm"));
            
            ObjectMapper objectMapper = new ObjectMapper();
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
            
            Map<String, Integer> thermometerAlarmCount = new HashMap<>();
            
            try {
                while (true) {
                    ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
                    for (ConsumerRecord<String, String> record : records) {
                        try {
                            TemperatureAlarm alarm = objectMapper.readValue(record.value(), TemperatureAlarm.class);
                            
                            // Format the timestamp
                            Date date = new Date(alarm.getTimestamp());
                            String formattedDate = sdf.format(date);
                            
                            // Create alarm message
                            String alarmMessage = String.format(
                                "⚠️ ALARM: Thermometer %s reported %.2f°C at %s",
                                alarm.getThermometerId(), alarm.getTemperature(), formattedDate);
                            
                            // Update UI on the Event Dispatch Thread
                            SwingUtilities.invokeLater(() -> {
                                // Add new alarm to the top of the list
                                listModel.add(0, alarmMessage);
                                
                                // Keep list at a reasonable size
                                if (listModel.size() > MAX_ALARMS) {
                                    listModel.remove(MAX_ALARMS);
                                }
                                
                                // Update statistics
                                thermometerAlarmCount.put(
                                    alarm.getThermometerId(), 
                                    thermometerAlarmCount.getOrDefault(alarm.getThermometerId(), 0) + 1
                                );
                                
                                StringBuilder stats = new StringBuilder("Alarm Counts: ");
                                for (Map.Entry<String, Integer> entry : thermometerAlarmCount.entrySet()) {
                                    stats.append(entry.getKey()).append("=").append(entry.getValue()).append(", ");
                                }
                                // Remove trailing comma
                                if (stats.length() > 2) {
                                    stats.setLength(stats.length() - 2);
                                }
                                statsLabel.setText(stats.toString());
                            });
                        } catch (Exception e) {
                            System.err.println("Error processing alarm: " + e.getMessage());
                        }
                    }
                }
            } finally {
                consumer.close();
            }
        });
        
        consumerThread.setDaemon(true);
        consumerThread.start();
    }
}
