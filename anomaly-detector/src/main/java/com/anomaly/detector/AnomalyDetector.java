package com.anomaly.detector;

import com.anomaly.model.Transaction;
import com.anomaly.model.TransactionAlert;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.TypeAdapter;
import com.google.gson.stream.JsonReader;
import com.google.gson.stream.JsonWriter;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.connector.base.DeliveryGuarantee;
import org.apache.flink.connector.kafka.sink.KafkaRecordSerializationSchema;
import org.apache.flink.connector.kafka.sink.KafkaSink;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.streaming.api.windowing.assigners.SlidingProcessingTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;
import org.apache.flink.api.common.state.MapState;
import org.apache.flink.api.common.state.MapStateDescriptor;
import org.apache.flink.api.common.typeinfo.TypeHint;
import org.apache.flink.api.common.typeinfo.TypeInformation;
import org.apache.flink.configuration.Configuration;

import java.util.*;
import java.time.Instant;
import java.io.IOException;
import java.io.Serializable;

public class AnomalyDetector {

    private static final String INPUT_TOPIC = "transactions";
    private static final String OUTPUT_TOPIC = "alerts";
    private static final String BOOTSTRAP_SERVERS = "localhost:9092";

    // Replace the simple Gson initialization with a configured one
    private static final Gson gson = new GsonBuilder()
            .registerTypeAdapter(Instant.class, new InstantTypeAdapter())
            .create();

    // Add a custom TypeAdapter for Instant
    private static class InstantTypeAdapter extends TypeAdapter<Instant> {
        @Override
        public void write(JsonWriter out, Instant value) throws IOException {
            if (value == null) {
                out.nullValue();
            } else {
                out.value(value.toString());
            }
        }

        @Override
        public Instant read(JsonReader in) throws IOException {
            return Instant.parse(in.nextString());
        }
    }

    public static void main(String[] args) throws Exception {
        // Set up the execution environment
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        // Create Kafka source to replace deprecated FlinkKafkaConsumer
        KafkaSource<String> kafkaSource = KafkaSource.<String>builder()
                .setBootstrapServers(BOOTSTRAP_SERVERS)
                .setTopics(INPUT_TOPIC)
                .setGroupId("anomaly-detector")
                .setStartingOffsets(OffsetsInitializer.earliest())
                .setValueOnlyDeserializer(new SimpleStringSchema())
                .build();

        // Parse JSON transactions
        DataStream<Transaction> transactionStream = env
                .fromSource(kafkaSource, org.apache.flink.api.common.eventtime.WatermarkStrategy.noWatermarks(), "Kafka Source")
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
                .window(SlidingProcessingTimeWindows.of(Time.minutes(5), Time.minutes(1)))
                .process(new AmountAnomalyDetector());

        // 2. Location anomaly - sudden change in location
        DataStream<TransactionAlert> locationAlerts = transactionStream
                .keyBy(Transaction::getCardId)
                .window(SlidingProcessingTimeWindows.of(Time.minutes(5), Time.minutes(1)))
                .process(new LocationAnomalyDetector());

        // 3. Frequency anomaly - unusual number of transactions in short time
        DataStream<TransactionAlert> frequencyAlerts = transactionStream
                .keyBy(Transaction::getCardId)
                .window(SlidingProcessingTimeWindows.of(Time.minutes(5), Time.minutes(1)))
                .process(new FrequencyAnomalyDetector());

        // Union all alert streams
        DataStream<TransactionAlert> allAlerts = amountAlerts
                .union(locationAlerts, frequencyAlerts);

        // Create KafkaSink to replace deprecated FlinkKafkaProducer
        KafkaSink<String> kafkaSink = KafkaSink.<String>builder()
                .setBootstrapServers(BOOTSTRAP_SERVERS)
                .setRecordSerializer(KafkaRecordSerializationSchema.builder()
                        .setTopic(OUTPUT_TOPIC)
                        .setValueSerializationSchema(new SimpleStringSchema())
                        .build())
                .setDeliverGuarantee(DeliveryGuarantee.AT_LEAST_ONCE)
                .build();

        // Convert alerts to JSON and send to Kafka
        allAlerts
                .map(alert -> gson.toJson(alert))
                .sinkTo(kafkaSink);

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

            // Check for anomalies (transactions that are more than 1.7 standard deviations from mean)
            for (Transaction transaction : transactionList) {
                if (stdDeviation > 0 && Math.abs(transaction.getAmount() - averageAmount) > 2 * stdDeviation && transaction.getAmount() > averageAmount && transaction.getAmount() > 1000) {
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

        private transient MapState<String, Set<LocationPoint>> knownLocations;
        private static final int MAX_KNOWN_LOCATIONS = 5; // Limit known locations to avoid memory issues
        private static final double ANOMALY_DISTANCE_THRESHOLD = 50.0; // Threshold in km
        private static final int MIN_LOCATIONS_FOR_DETECTION = 3; // Minimum known locations before detecting anomalies

        @Override
        public void open(Configuration parameters) throws Exception {
            MapStateDescriptor<String, Set<LocationPoint>> descriptor =
                new MapStateDescriptor<>(
                    "knownLocations",
                    TypeInformation.of(String.class),
                    TypeInformation.of(new TypeHint<Set<LocationPoint>>() {})
                );
            knownLocations = getRuntimeContext().getMapState(descriptor);
        }

        @Override
        public void process(String cardId, Context context, Iterable<Transaction> transactions,
                           Collector<TransactionAlert> out) throws Exception {
            List<Transaction> transactionList = new ArrayList<>();
            transactions.forEach(transactionList::add);

            if (transactionList.isEmpty()) return;

            // Get or create location set for this card
            Set<LocationPoint> cardKnownLocations;
            if (knownLocations.contains(cardId)) {
                cardKnownLocations = knownLocations.get(cardId);
                System.out.println("Card " + cardId + " has " + cardKnownLocations.size() + " known locations");
            } else {
                cardKnownLocations = new HashSet<>();
                System.out.println("New card detected: " + cardId + ", initializing known locations");
            }

            // Process each transaction
            for (Transaction transaction : transactionList) {
                LocationPoint currentPoint = new LocationPoint(transaction.getLatitude(), transaction.getLongitude());

                // First few transactions establish the baseline locations
                if (cardKnownLocations.size() < MIN_LOCATIONS_FOR_DETECTION) {
                    System.out.println("Building baseline for card " + cardId + ", adding location #" +
                                      (cardKnownLocations.size() + 1) + " to known locations");

                    // Check if this location is already very close to a known location before adding
                    boolean isVeryCloseToKnown = false;
                    for (LocationPoint knownPoint : cardKnownLocations) {
                        if (calculateDistance(currentPoint, knownPoint) < 2.0) { // Within 2km = same area
                            isVeryCloseToKnown = true;
                            System.out.println("Location is very close to existing baseline location, not adding duplicate");
                            break;
                        }
                    }

                    // Only add distinct baseline locations
                    if (!isVeryCloseToKnown) {
                        cardKnownLocations.add(currentPoint);
                    }

                    // We're still building the baseline, don't check for anomalies yet
                    continue;
                }

                // Check distance to known locations
                double closestDistance = Double.MAX_VALUE;
                LocationPoint closestPoint = null;

                for (LocationPoint knownPoint : cardKnownLocations) {
                    double distance = calculateDistance(currentPoint, knownPoint);
                    if (distance < closestDistance) {
                        closestDistance = distance;
                        closestPoint = knownPoint;
                    }
                }

                System.out.println("CARD " + cardId + ": Transaction at " + currentPoint + ", closest known location: " +
                                  closestPoint + " (" + String.format("%.2f", closestDistance) + " km)");

                // Detect anomaly if transaction is far from all known locations
                if (closestDistance > ANOMALY_DISTANCE_THRESHOLD) {
                    System.out.println("⚠️ LOCATION ANOMALY DETECTED: Distance " +
                                      String.format("%.2f", closestDistance) + "km exceeds threshold of " +
                                      ANOMALY_DISTANCE_THRESHOLD + "km");

                    out.collect(new TransactionAlert(
                            "LOCATION_ANOMALY",
                            transaction.getCardId(),
                            transaction.getUserId(),
                            transaction.getAmount(),
                            transaction.getLatitude(),
                            transaction.getLongitude(),
                            transaction.getTimestamp(),
                            "Unusual transaction location: " + String.format("%.2f", closestDistance) +
                            "km from nearest known location"
                    ));

                    // Don't automatically add anomalous locations to known locations
                } else {
                    // Check if this location is already very close to a known location
                    boolean isVeryCloseToKnown = false;
                    for (LocationPoint knownPoint : cardKnownLocations) {
                        if (calculateDistance(currentPoint, knownPoint) < 2.0) { // Within 2km = same area
                            isVeryCloseToKnown = true;
                            break;
                        }
                    }

                    // Only add distinct new locations, up to our maximum
                    if (!isVeryCloseToKnown && cardKnownLocations.size() < MAX_KNOWN_LOCATIONS) {
                        cardKnownLocations.add(currentPoint);
                        System.out.println("Added new location to known locations: " + currentPoint);
                    }
                }
            }

            // Update the state
            knownLocations.put(cardId, cardKnownLocations);
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

        private static class LocationPoint implements Serializable {
            private static final long serialVersionUID = 1L;
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

            @Override
            public String toString() {
                return "LocationPoint{" +
                        "lat=" + latitude +
                        ", lon=" + longitude +
                        '}';
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
