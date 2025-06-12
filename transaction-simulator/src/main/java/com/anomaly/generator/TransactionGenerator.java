package com.anomaly.generator;

import com.anomaly.model.Transaction;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.ThreadLocalRandom;

public class TransactionGenerator {
    private static final int NUM_CARDS = 10000;
    private static final int NUM_USERS = 5000; // Assuming each user has ~2 cards on average
    private static final Map<String, Set<LocationPoint>> cardLocations = new HashMap<>();
    private static final Map<String, Double> cardLimits = new HashMap<>();
    private static final Map<String, String> cardToUser = new HashMap<>();
    private static final List<String> cardIds = new ArrayList<>();
    private static final List<String> userIds = new ArrayList<>();

    // Anomaly types
    private static final int ANOMALY_NONE = 0;
    private static final int ANOMALY_AMOUNT = 1;
    private static final int ANOMALY_LOCATION = 2;
    private static final int ANOMALY_FREQUENCY = 3;

    // Probability of generating an anomaly (1%)
    private static final double ANOMALY_PROBABILITY = 0.05;

    // Initialize card and user data
    static {
        // Generate user IDs
        for (int i = 0; i < NUM_USERS; i++) {
            userIds.add("USER_" + String.format("%05d", i));
        }

        // Generate card IDs and assign to users
        for (int i = 0; i < NUM_CARDS; i++) {
            String cardId = "CARD_" + String.format("%05d", i);
            cardIds.add(cardId);
            String userId = userIds.get(ThreadLocalRandom.current().nextInt(NUM_USERS));
            cardToUser.put(cardId, userId);

            // Initialize empty set of locations for this card
            cardLocations.put(cardId, new HashSet<>());

            // Assign random limit between $1,000 and $20,000
            cardLimits.put(cardId, 1000.0 + ThreadLocalRandom.current().nextDouble() * 19000.0);
        }
    }

    public Transaction generateTransaction(boolean forceAnomaly, int anomalyType) {
        // Select a random card
        String cardId = cardIds.get(ThreadLocalRandom.current().nextInt(NUM_CARDS));
        String userId = cardToUser.get(cardId);
        double availableLimit = cardLimits.get(cardId);

        // Determine if this should be an anomaly
        int actualAnomalyType = ANOMALY_NONE;
        if (forceAnomaly) {
            actualAnomalyType = (anomalyType >= 0 && anomalyType <= 3) ?
                                anomalyType : ThreadLocalRandom.current().nextInt(1, 4);
        } else if (ThreadLocalRandom.current().nextDouble() < ANOMALY_PROBABILITY) {
            double roll = ThreadLocalRandom.current().nextDouble();
            if (roll < 0.4) {
                actualAnomalyType = ANOMALY_LOCATION;
            } else if (roll < 0.7) {
                actualAnomalyType = ANOMALY_AMOUNT;
            } else {
                actualAnomalyType = ANOMALY_FREQUENCY;
            }
        }

        // Get or generate location
        LocationPoint location = getLocationForCard(cardId, actualAnomalyType == ANOMALY_LOCATION);
        double latitude = location.latitude;
        double longitude = location.longitude;

        // Generate transaction amount
        double amount;
        if (actualAnomalyType == ANOMALY_AMOUNT) {
            // Generate anomalously high amount (50-90% of available limit)
            amount = availableLimit * (0.5 + ThreadLocalRandom.current().nextDouble() * 0.4);
        } else {
            // Normal amount (1-10% of available limit)
            amount = availableLimit * (0.01 + ThreadLocalRandom.current().nextDouble() * 0.09);
        }

        // Update available limit
        double newLimit = availableLimit - amount;
        cardLimits.put(cardId, newLimit > 0 ? newLimit : 0);

        // Create transaction
        Transaction transaction = new Transaction(
            cardId,
            userId,
            latitude,
            longitude,
            amount,
            newLimit,
            Instant.now()
        );

        return transaction;
    }

    private LocationPoint getLocationForCard(String cardId, boolean generateAnomaly) {
        Set<LocationPoint> locations = cardLocations.get(cardId);

        if (locations.isEmpty() || generateAnomaly) {
            // Generate a random worldwide location
            double latitude = ThreadLocalRandom.current().nextDouble(-90, 90);
            double longitude = ThreadLocalRandom.current().nextDouble(-180, 180);
            LocationPoint newLocation = new LocationPoint(latitude, longitude);

            // Store this location for future use unless it's an anomaly
            if (!generateAnomaly) {
                locations.add(newLocation);
            }

            return newLocation;
        } else {
            // Pick a random location from the card's history
            LocationPoint[] locArray = locations.toArray(new LocationPoint[0]);
            return locArray[ThreadLocalRandom.current().nextInt(locArray.length)];
        }
    }

    // Method to simulate frequency anomaly by generating multiple transactions in short succession
    public List<Transaction> generateFrequencyAnomaly(String specificCardId) {
        List<Transaction> transactions = new ArrayList<>();
        String cardId = specificCardId != null ?
                      specificCardId : cardIds.get(ThreadLocalRandom.current().nextInt(NUM_CARDS));

        // Generate 5-10 transactions in quick succession
        int numTransactions = ThreadLocalRandom.current().nextInt(5, 11);
        for (int i = 0; i < numTransactions; i++) {
            transactions.add(generateTransactionForCard(cardId, false, ANOMALY_NONE));
        }

        return transactions;
    }

    private Transaction generateTransactionForCard(String cardId, boolean forceAnomaly, int anomalyType) {
        String userId = cardToUser.get(cardId);
        double availableLimit = cardLimits.get(cardId);

        // Get location
        LocationPoint location = getLocationForCard(cardId, forceAnomaly && anomalyType == ANOMALY_LOCATION);
        double latitude = location.latitude;
        double longitude = location.longitude;

        // Generate amount
        double amount;
        if (forceAnomaly && anomalyType == ANOMALY_AMOUNT) {
            amount = availableLimit * (0.5 + ThreadLocalRandom.current().nextDouble() * 0.4);
        } else {
            amount = availableLimit * (0.01 + ThreadLocalRandom.current().nextDouble() * 0.09);
        }

        // Update available limit
        double newLimit = availableLimit - amount;
        cardLimits.put(cardId, newLimit > 0 ? newLimit : 0);

        return new Transaction(
            cardId,
            userId,
            latitude,
            longitude,
            amount,
            newLimit,
            Instant.now()
        );
    }

    private static class LocationPoint {
        final double latitude;
        final double longitude;

        LocationPoint(double latitude, double longitude) {
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
