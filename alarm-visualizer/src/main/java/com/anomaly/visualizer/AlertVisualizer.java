package com.anomaly.visualizer;

import com.anomaly.model.TransactionAlert;
import com.google.gson.Gson;
import org.apache.kafka.clients.consumer.*;
import org.apache.kafka.common.serialization.StringDeserializer;
//import org.slf4j.Logger;
//import org.slf4j.LoggerFactory;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.time.Duration;
import java.time.Instant;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.List;

public class AlertVisualizer {
    //private static final Logger logger = LoggerFactory.getLogger(AlertVisualizer.class);
    private static final String BOOTSTRAP_SERVERS = "localhost:9092";
    private static final String GROUP_ID = "alert-visualizer-group";
    private static final String TOPIC = "alerts";
    private static final Gson gson = new Gson();
    
    // UI Components
    private static JFrame frame;
    private static JTable alertTable;
    private static DefaultTableModel tableModel;
    private static JTextArea detailArea;
    private static final List<TransactionAlert> allAlerts = new ArrayList<>();
    private static final DateTimeFormatter formatter = 
            DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss").withZone(ZoneId.systemDefault());
    
    public static void main(String[] args) {
        setupUI();
        
        // Create consumer properties
        Properties properties = new Properties();
        properties.setProperty(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVERS);
        properties.setProperty(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        properties.setProperty(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        properties.setProperty(ConsumerConfig.GROUP_ID_CONFIG, GROUP_ID);
        properties.setProperty(ConsumerConfig.AUTO_OFFSET_RESET_CONFIG, "earliest");
        
        // Create consumer
        KafkaConsumer<String, String> consumer = new KafkaConsumer<>(properties);
        
        // Subscribe to topic
        consumer.subscribe(Collections.singletonList(TOPIC));
        
        // Add shutdown hook
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            //logger.info("Shutting down alert visualizer...");
            consumer.close();
            //logger.info("Alert visualizer closed");
        }));
        
        // Poll for new alerts
        try {
            while (true) {
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
                
                boolean newAlerts = false;
                for (ConsumerRecord<String, String> record : records) {
                    // Parse the alert
                    TransactionAlert alert = gson.fromJson(record.value(), TransactionAlert.class);
                    addAlert(alert);
                    newAlerts = true;
                    
                    // Display notification for new alert
                    displayNotification(alert);
                }
                
                // Update the UI if new alerts arrived
                if (newAlerts) {
                    updateAlertTable();
                }
            }
        } finally {
            consumer.close();
        }
    }
    
    private static void setupUI() {
        frame = new JFrame("Transaction Alert Visualizer");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(1024, 768);
        
        // Create table with columns
        String[] columnNames = {"Time", "Alert Type", "Card ID", "User ID", "Amount", "Message"};
        tableModel = new DefaultTableModel(columnNames, 0);
        alertTable = new JTable(tableModel);
        alertTable.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        
        // Add selection listener to show details when an alert is selected
        alertTable.getSelectionModel().addListSelectionListener(e -> {
            if (!e.getValueIsAdjusting()) {
                int selectedRow = alertTable.getSelectedRow();
                if (selectedRow >= 0 && selectedRow < allAlerts.size()) {
                    showAlertDetails(allAlerts.get(selectedRow));
                }
            }
        });
        
        JScrollPane tableScrollPane = new JScrollPane(alertTable);
        
        // Create detail panel
        detailArea = new JTextArea();
        detailArea.setEditable(false);
        JScrollPane detailScrollPane = new JScrollPane(detailArea);
        
        // Create map visualization panel
        JPanel mapPanel = new JPanel() {
            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                drawMap(g);
            }
        };
        
        // Create split panes for layout
        JSplitPane mainSplitPane = new JSplitPane(JSplitPane.VERTICAL_SPLIT, 
                tableScrollPane, new JSplitPane(JSplitPane.HORIZONTAL_SPLIT, detailScrollPane, mapPanel));
        mainSplitPane.setDividerLocation(300);
        ((JSplitPane)mainSplitPane.getBottomComponent()).setDividerLocation(500);
        
        frame.add(mainSplitPane);
        frame.setVisible(true);
    }
    
    private static void addAlert(TransactionAlert alert) {
        synchronized (allAlerts) {
            allAlerts.add(0, alert); // Add at the beginning for newest first
        }
    }
    
    private static void updateAlertTable() {
        SwingUtilities.invokeLater(() -> {
            tableModel.setRowCount(0); // Clear table
            
            synchronized (allAlerts) {
                for (TransactionAlert alert : allAlerts) {
                    String formattedTime = formatter.format(alert.getAlertTime());
                    tableModel.addRow(new Object[]{
                            formattedTime,
                            alert.getAlertType(),
                            alert.getCardId(),
                            alert.getUserId(),
                            String.format("$%.2f", alert.getAmount()),
                            alert.getMessage()
                    });
                }
            }
        });
    }
    
    private static void showAlertDetails(TransactionAlert alert) {
        SwingUtilities.invokeLater(() -> {
            StringBuilder sb = new StringBuilder();
            sb.append("ALERT DETAILS\n");
            sb.append("============================================\n\n");
            sb.append("Alert Type: ").append(alert.getAlertType()).append("\n");
            sb.append("Alert Time: ").append(formatter.format(alert.getAlertTime())).append("\n");
            sb.append("Transaction Time: ").append(formatter.format(alert.getTimestamp())).append("\n\n");
            sb.append("Card ID: ").append(alert.getCardId()).append("\n");
            sb.append("User ID: ").append(alert.getUserId()).append("\n");
            sb.append("Transaction Amount: $").append(String.format("%.2f", alert.getAmount())).append("\n\n");
            sb.append("Location: ").append(alert.getLatitude()).append(", ").append(alert.getLongitude()).append("\n\n");
            sb.append("Alert Message: ").append(alert.getMessage()).append("\n");
            
            detailArea.setText(sb.toString());
            frame.repaint(); // Trigger map redraw to highlight selected alert
        });
    }
    
    private static void drawMap(Graphics g) {
        Graphics2D g2d = (Graphics2D) g;
        int width = g2d.getClipBounds().width;
        int height = g2d.getClipBounds().height;
        
        // Draw world map (simplified)
        g2d.setColor(Color.LIGHT_GRAY);
        g2d.fillRect(0, 0, width, height);
        g2d.setColor(Color.DARK_GRAY);
        g2d.drawRect(0, 0, width - 1, height - 1);
        
        // Draw grid lines
        g2d.setColor(Color.GRAY);
        for (int i = 0; i < width; i += 50) {
            g2d.drawLine(i, 0, i, height);
        }
        for (int i = 0; i < height; i += 50) {
            g2d.drawLine(0, i, width, i);
        }
        
        // Get selected alert
        int selectedRow = alertTable.getSelectedRow();
        TransactionAlert selectedAlert = null;
        if (selectedRow >= 0 && selectedRow < allAlerts.size()) {
            selectedAlert = allAlerts.get(selectedRow);
        }
        
        // Draw alert points
        synchronized (allAlerts) {
            for (TransactionAlert alert : allAlerts) {
                // Map lat/lon to screen coordinates
                int x = (int) ((alert.getLongitude() + 180) / 360 * width);
                int y = (int) ((90 - alert.getLatitude()) / 180 * height);
                
                // Color by alert type
                if (alert.getAlertType().equals("AMOUNT_ANOMALY")) {
                    g2d.setColor(Color.RED);
                } else if (alert.getAlertType().equals("LOCATION_ANOMALY")) {
                    g2d.setColor(Color.BLUE);
                } else {
                    g2d.setColor(Color.ORANGE);
                }
                
                // Make selected alert larger
                if (alert == selectedAlert) {
                    g2d.fillOval(x - 8, y - 8, 16, 16);
                } else {
                    g2d.fillOval(x - 4, y - 4, 8, 8);
                }
            }
        }
        
        // Draw legend
        g2d.setColor(Color.BLACK);
        g2d.drawString("Legend:", width - 150, 20);
        g2d.setColor(Color.RED);
        g2d.fillOval(width - 140, 30, 10, 10);
        g2d.setColor(Color.BLACK);
        g2d.drawString("Amount Anomaly", width - 125, 40);
        g2d.setColor(Color.BLUE);
        g2d.fillOval(width - 140, 50, 10, 10);
        g2d.setColor(Color.BLACK);
        g2d.drawString("Location Anomaly", width - 125, 60);
        g2d.setColor(Color.ORANGE);
        g2d.fillOval(width - 140, 70, 10, 10);
        g2d.setColor(Color.BLACK);
        g2d.drawString("Frequency Anomaly", width - 125, 80);
    }
    
    private static void displayNotification(TransactionAlert alert) {
        SwingUtilities.invokeLater(() -> {
            // Make a simple notification window
            JDialog dialog = new JDialog(frame, "New Alert!", false);
            dialog.setSize(400, 150);
            dialog.setLocationRelativeTo(frame);
            
            JPanel panel = new JPanel(new BorderLayout());
            JLabel label = new JLabel("<html><b>" + alert.getAlertType() + "</b><br>" + 
                                     alert.getMessage() + "<br>Card: " + alert.getCardId() + "</html>");
            label.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));
            panel.add(label, BorderLayout.CENTER);
            
            JButton closeButton = new JButton("Dismiss");
            closeButton.addActionListener(e -> dialog.dispose());
            JPanel buttonPanel = new JPanel();
            buttonPanel.add(closeButton);
            panel.add(buttonPanel, BorderLayout.SOUTH);
            
            dialog.add(panel);
            dialog.setVisible(true);
            
            // Auto-dismiss after 5 seconds
            javax.swing.Timer timer = new javax.swing.Timer(5000, e -> dialog.dispose());
            timer.setRepeats(false);
            timer.start();
        });
    }
}
