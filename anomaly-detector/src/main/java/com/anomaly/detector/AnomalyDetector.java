package com.anomaly.detector;

import com.anomaly.model.Transaction;
import com.anomaly.model.TransactionAlert;
import com.google.gson.Gson;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.streaming.api.windowing.assigners.SlidingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer;
import org.apache.flink.streaming.connectors.kafka.FlinkKafkaProducer;
import org.apache.flink.util.Collector;

import java.util.*;
import java.time.Instant;

public class AnomalyDetector {

    private static final String INPUT_TOPIC = "transactions";
    private static final String OUTPUT_TOPIC = "alerts";
    private static final String BOOTSTRAP_SERVERS = "localhost:9092";
    private static final Gson gson = new Gson();

    public static void main(String[] args) throws Exception {
        // Set up the execution environment
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        // Configure Kafka consumer
        Properties properties = new Properties();
        properties.setProperty("bootstrap.servers", BOOTSTRAP_SERVERS);
        properties.setProperty("group.id", "anomaly-detector");

        // Create Kafka consumer
        FlinkKafkaConsumer<String> consumer = new FlinkKafkaConsumer<>(
                INPUT_TOPIC,
                new SimpleStringSchema(),
                properties
        );

        // Parse JSON transactions
        DataStream<Transaction> transactionStream = env
                .addSource(consumer)
                .map(new MapFunction<String, Transaction>() {
                    @Override
                    public Transaction map(String value) throws Exception {
                        return gson.fromJson(value, Transaction.class);
                    }
                });

        // Detect anomalies based on different metrics
        // 1. Amount anomaly - sudden high-value transactions
        DataStream<TransactionAlert> amountAlerts = transactionStream
                .keyBy(Transaction::getCardId)
                .window(SlidingProcessingTimeWindows.of(Time.minutes(10), Time.minutes(1)))
                .process(new AmountAnomalyDetector());

        // 2. Location anomaly - sudden change in location
        DataStream<TransactionAlert> locationAlerts = transactionStream
                .keyBy(Transaction::getCardId)
                .window(SlidingProcessingTimeWindows.of(Time.minutes(10), Time.minutes(1)))
                .process(new LocationAnomalyDetector());

        // 3. Frequency anomaly - unusual number of transactions in short time
        DataStream<TransactionAlert> frequencyAlerts = transactionStream
                .keyBy(Transaction::getCardId)
                .window(SlidingProcessingTimeWindows.of(Time.minutes(5), Time.minutes(1)))
                .process(new FrequencyAnomalyDetector());

        // Union all alert streams
        DataStream<TransactionAlert> allAlerts = amountAlerts
                .union(locationAlerts, frequencyAlerts);

        // Convert alerts to JSON and send to Kafka
        allAlerts
                .map(alert -> gson.toJson(alert))
                .addSink(new FlinkKafkaProducer<>(
                        OUTPUT_TOPIC,
                        new SimpleStringSchema(),
                        properties
                ));

        // Execute the Flink job
        env.execute("Credit Card Transaction Anomaly Detection");
    }

    // Detector for unusual transaction amounts
    public static class AmountAnomalyDetector 
            extends ProcessWindowFunction<Transaction, TransactionAlert, String, TimeWindow> {
        
        @Override
        public void process(String cardId, Context context, Iterable<Transaction> transactions, 
                           Collector<TransactionAlert> out) {
            List<Transaction> transactionList = new ArrayList<>();
            transactions.forEach(transactionList::add);
            
            if (transactionList.isEmpty()) return;
            
            // Calculate statistics
            double averageAmount = transactionList.stream()
                    .mapToDouble(Transaction::getAmount)
                    .average()
                    .orElse(0);
            
            double stdDeviation = calculateStdDeviation(transactionList, averageAmount);
            
            // Check for anomalies (transactions that are more than 3 standard deviations from mean)
            for (Transaction transaction : transactionList) {
                if (stdDeviation > 0 && Math.abs(transaction.getAmount() - averageAmount) > 3 * stdDeviation) {
                    out.collect(new TransactionAlert(
                            "AMOUNT_ANOMALY",
                            transaction.getCardId(),
                            transaction.getUserId(),
                            transaction.getAmount(),
                            transaction.getLatitude(),
                            transaction.getLongitude(),
                            transaction.getTimestamp(),
                            "Unusual transaction amount detected: $" + transaction.getAmount() + 
                            " (Average: $" + String.format("%.2f", averageAmount) + ")"
                    ));
                }
            }
        }
        
        private double calculateStdDeviation(List<Transaction> transactions, double mean) {
            return Math.sqrt(transactions.stream()
                    .mapToDouble(t -> Math.pow(t.getAmount() - mean, 2))
                    .average()
                    .orElse(0));
        }
    }

    // Detector for unusual transaction locations
    public static class LocationAnomalyDetector 
            extends ProcessWindowFunction<Transaction, TransactionAlert, String, TimeWindow> {
        
        // Map to store frequent locations for each card
        private final Map<String, Set<LocationPoint>> cardLocations = new HashMap<>();
        
        @Override
        public void process(String cardId, Context context, Iterable<Transaction> transactions, 
                           Collector<TransactionAlert> out) {
            List<Transaction> transactionList = new ArrayList<>();
            transactions.forEach(transactionList::add);
            
            if (transactionList.isEmpty()) return;
            
            // Get or create location set for this card
            Set<LocationPoint> frequentLocations = cardLocations.computeIfAbsent(cardId, k -> new HashSet<>());
            
            // Process each transaction
            for (Transaction transaction : transactionList) {
                LocationPoint currentPoint = new LocationPoint(transaction.getLatitude(), transaction.getLongitude());
                
                // If we have at least 3 frequent locations for this card
                if (frequentLocations.size() >= 3) {
                    boolean isNearKnownLocation = false;
                    
                    // Check if current location is near any known frequent location
                    for (LocationPoint knownPoint : frequentLocations) {
                        if (calculateDistance(currentPoint, knownPoint) < 50) { // Less than 50km
                            isNearKnownLocation = true;
                            break;
                        }
                    }
                    
                    // If not near any known location, it might be an anomaly
                    if (!isNearKnownLocation) {
                        out.collect(new TransactionAlert(
                                "LOCATION_ANOMALY",
                                transaction.getCardId(),
                                transaction.getUserId(),
                                transaction.getAmount(),
                                transaction.getLatitude(),
                                transaction.getLongitude(),
                                transaction.getTimestamp(),
                                "Unusual transaction location detected at: " + 
                                transaction.getLatitude() + ", " + transaction.getLongitude()
                        ));
                    }
                }
                
                // Add current location to frequent locations (max 10 locations per card)
                if (frequentLocations.size() < 10) {
                    frequentLocations.add(currentPoint);
                }
            }
        }
        
        // Calculate distance between two points using Haversine formula (in km)
        private double calculateDistance(LocationPoint p1, LocationPoint p2) {
            final int R = 6371; // Earth radius in km
            
            double latDistance = Math.toRadians(p2.latitude - p1.latitude);
            double lonDistance = Math.toRadians(p2.longitude - p1.longitude);
            
            double a = Math.sin(latDistance / 2) * Math.sin(latDistance / 2)
                    + Math.cos(Math.toRadians(p1.latitude)) * Math.cos(Math.toRadians(p2.latitude))
                    * Math.sin(lonDistance / 2) * Math.sin(lonDistance / 2);
            
            double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
            
            return R * c;
        }
        
        private static class LocationPoint {
            private final double latitude;
            private final double longitude;
            
            public LocationPoint(double latitude, double longitude) {
                this.latitude = latitude;
                this.longitude = longitude;
            }
            
            @Override
            public boolean equals(Object o) {
                if (this == o) return true;
                if (o == null || getClass() != o.getClass()) return false;
                LocationPoint that = (LocationPoint) o;
                return Double.compare(that.latitude, latitude) == 0 &&
                        Double.compare(that.longitude, longitude) == 0;
            }
            
            @Override
            public int hashCode() {
                return Objects.hash(latitude, longitude);
            }
        }
    }

    // Detector for unusual transaction frequency
    public static class FrequencyAnomalyDetector 
            extends ProcessWindowFunction<Transaction, TransactionAlert, String, TimeWindow> {
        
        @Override
        public void process(String cardId, Context context, Iterable<Transaction> transactions, 
                           Collector<TransactionAlert> out) {
            List<Transaction> transactionList = new ArrayList<>();
            transactions.forEach(transactionList::add);
            
            // Get window info
            long windowStart = context.window().getStart();
            long windowEnd = context.window().getEnd();
            long windowSizeMinutes = (windowEnd - windowStart) / (1000 * 60);
            
            // If there are more than 5 transactions in 5 minutes for the same card, flag it
            if (transactionList.size() > 5) {
                Transaction latestTransaction = transactionList.stream()
                        .max(Comparator.comparing(Transaction::getTimestamp))
                        .orElse(transactionList.get(0));
                
                out.collect(new TransactionAlert(
                        "FREQUENCY_ANOMALY",
                        latestTransaction.getCardId(),
                        latestTransaction.getUserId(),
                        latestTransaction.getAmount(),
                        latestTransaction.getLatitude(),
                        latestTransaction.getLongitude(),
                        latestTransaction.getTimestamp(),
                        "Unusual transaction frequency detected: " + transactionList.size() + 
                        " transactions in " + windowSizeMinutes + " minutes"
                ));
            }
        }
    }
}
