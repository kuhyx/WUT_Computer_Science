package com.anomaly.model;

import java.time.Instant;
import java.util.Objects;

public class Transaction {
    private final String cardId;
    private final String userId;
    private final double latitude;
    private final double longitude;
    private final double amount;
    private final double availableLimit;
    private final Instant timestamp;

    public Transaction(String cardId, String userId, double latitude, double longitude, 
                      double amount, double availableLimit, Instant timestamp) {
        this.cardId = cardId;
        this.userId = userId;
        this.latitude = latitude;
        this.longitude = longitude;
        this.amount = amount;
        this.availableLimit = availableLimit;
        this.timestamp = timestamp;
    }

    public String getCardId() {
        return cardId;
    }

    public String getUserId() {
        return userId;
    }

    public double getLatitude() {
        return latitude;
    }

    public double getLongitude() {
        return longitude;
    }

    public double getAmount() {
        return amount;
    }

    public double getAvailableLimit() {
        return availableLimit;
    }

    public Instant getTimestamp() {
        return timestamp;
    }

    @Override
    public String toString() {
        return "Transaction{" +
                "cardId='" + cardId + '\'' +
                ", userId='" + userId + '\'' +
                ", latitude=" + latitude +
                ", longitude=" + longitude +
                ", amount=" + amount +
                ", availableLimit=" + availableLimit +
                ", timestamp=" + timestamp +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Transaction that = (Transaction) o;
        return Double.compare(that.latitude, latitude) == 0 &&
               Double.compare(that.longitude, longitude) == 0 &&
               Double.compare(that.amount, amount) == 0 &&
               Double.compare(that.availableLimit, availableLimit) == 0 &&
               Objects.equals(cardId, that.cardId) &&
               Objects.equals(userId, that.userId) &&
               Objects.equals(timestamp, that.timestamp);
    }

    @Override
    public int hashCode() {
        return Objects.hash(cardId, userId, latitude, longitude, amount, availableLimit, timestamp);
    }
}
