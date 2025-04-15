package com.anomaly.consumer;

import com.anomaly.model.Transaction;
import com.google.gson.Gson;
import org.apache.kafka.clients.consumer.*;
import org.apache.kafka.common.serialization.StringDeserializer;

import javax.swing.*;
import java.awt.*;
import java.time.Duration;
import java.util.*;
import java.util.List;

public class TransactionConsumer {
    //private static final Logger logger = LoggerFactory.getLogger(TransactionConsumer.class);
    private static final String BOOTSTRAP_SERVERS = "localhost:9092";
    private static final String GROUP_ID = "transaction-consumer-group";
    private static final String TOPIC = "transactions";
    private static final Gson gson = new Gson();
    
    // UI Components
    private static JFrame frame;
    private static JTextArea logArea;
    private static JPanel chartPanel;
    private static final int MAX_DISPLAYED_TRANSACTIONS = 100;
    private static final List<Transaction> recentTransactions = new ArrayList<>();
    
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
            //logger.info("Shutting down consumer...");
            consumer.close();
            //logger.info("Consumer closed");
        }));
        
        // Poll for new data
        try {
            while (true) {
                ConsumerRecords<String, String> records = consumer.poll(Duration.ofMillis(100));
                
                for (ConsumerRecord<String, String> record : records) {
                    logMessage("Received: Key: " + record.key() + ", Value: " + record.value());
                    
                    // Parse the transaction
                    Transaction transaction = gson.fromJson(record.value(), Transaction.class);
                    addTransaction(transaction);
                }
                
                // Update the visualization
                if (!records.isEmpty()) {
                    updateChart();
                }
            }
        } finally {
            consumer.close();
        }
    }
    
    private static void setupUI() {
        frame = new JFrame("Transaction Visualizer");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(800, 600);
        
        // Create log area
        logArea = new JTextArea();
        logArea.setEditable(false);
        JScrollPane scrollPane = new JScrollPane(logArea);
        scrollPane.setPreferredSize(new Dimension(800, 200));
        
        // Create chart panel
        chartPanel = new JPanel() {
            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                drawChart(g);
            }
        };
        chartPanel.setPreferredSize(new Dimension(800, 400));
        
        // Add components to frame
        frame.setLayout(new BorderLayout());
        frame.add(scrollPane, BorderLayout.SOUTH);
        frame.add(chartPanel, BorderLayout.CENTER);
        
        frame.setVisible(true);
    }
    
    private static void logMessage(String message) {
        SwingUtilities.invokeLater(() -> {
            logArea.append(message + "\n");
            logArea.setCaretPosition(logArea.getDocument().getLength());
        });
    }
    
    private static void addTransaction(Transaction transaction) {
        synchronized (recentTransactions) {
            recentTransactions.add(transaction);
            if (recentTransactions.size() > MAX_DISPLAYED_TRANSACTIONS) {
                recentTransactions.remove(0);
            }
        }
    }
    
    private static void updateChart() {
        SwingUtilities.invokeLater(() -> chartPanel.repaint());
    }
    
    private static void drawChart(Graphics g) {
        Graphics2D g2d = (Graphics2D) g;
        int width = chartPanel.getWidth();
        int height = chartPanel.getHeight();
        
        // Clear the background
        g2d.setColor(Color.WHITE);
        g2d.fillRect(0, 0, width, height);
        
        synchronized (recentTransactions) {
            if (recentTransactions.isEmpty()) return;
            
            // Find max amount for scaling
            double maxAmount = recentTransactions.stream()
                    .mapToDouble(Transaction::getAmount)
                    .max()
                    .orElse(1.0);
            
            // Draw axes
            g2d.setColor(Color.BLACK);
            g2d.drawLine(50, height - 50, width - 50, height - 50); // X-axis
            g2d.drawLine(50, 50, 50, height - 50); // Y-axis
            
            // Draw labels
            g2d.drawString("Time →", width - 70, height - 20);
            g2d.drawString("Amount", 10, 40);
            g2d.drawString("$" + Math.round(maxAmount), 10, 60);
            
            // Draw transactions as points
            int xStep = (width - 100) / Math.max(1, recentTransactions.size() - 1);
            int x = 50;
            
            for (Transaction transaction : recentTransactions) {
                int y = height - 50 - (int) ((transaction.getAmount() / maxAmount) * (height - 100));
                
                // Color based on available limit percentage
                double limitPercentage = transaction.getAvailableLimit() / 
                                        (transaction.getAmount() + transaction.getAvailableLimit());
                
                if (limitPercentage < 0.3) {
                    g2d.setColor(Color.RED);
                } else if (limitPercentage < 0.6) {
                    g2d.setColor(Color.ORANGE);
                } else {
                    g2d.setColor(Color.GREEN);
                }
                
                g2d.fillOval(x - 3, y - 3, 6, 6);
                x += xStep;
            }
        }
    }
}
