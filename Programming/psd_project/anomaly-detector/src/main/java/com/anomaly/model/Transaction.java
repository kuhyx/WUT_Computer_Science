package com.anomaly.model;

import java.time.Instant;

/**
 * Represents a financial transaction with location data.
 */
public class Transaction {
    private String cardId;
    private String userId;
    private double amount;
    private double latitude;
    private double longitude;
    private Instant timestamp;
    
    // Default constructor for deserialization
    public Transaction() {
    }
    
    public Transaction(String cardId, String userId, double amount, 
                      double latitude, double longitude, Instant timestamp) {
        this.cardId = cardId;
        this.userId = userId;
        this.amount = amount;
        this.latitude = latitude;
        this.longitude = longitude;
        this.timestamp = timestamp;
    }
    
    // Getters and setters
    public String getCardId() {
        return cardId;
    }
    
    public void setCardId(String cardId) {
        this.cardId = cardId;
    }
    
    public String getUserId() {
        return userId;
    }
    
    public void setUserId(String userId) {
        this.userId = userId;
    }
    
    public double getAmount() {
        return amount;
    }
    
    public void setAmount(double amount) {
        this.amount = amount;
    }
    
    public double getLatitude() {
        return latitude;
    }
    
    public void setLatitude(double latitude) {
        this.latitude = latitude;
    }
    
    public double getLongitude() {
        return longitude;
    }
    
    public void setLongitude(double longitude) {
        this.longitude = longitude;
    }
    
    public Instant getTimestamp() {
        return timestamp;
    }
    
    public void setTimestamp(Instant timestamp) {
        this.timestamp = timestamp;
    }
    
    @Override
    public String toString() {
        return "Transaction{" +
                "cardId='" + cardId + '\'' +
                ", userId='" + userId + '\'' +
                ", amount=" + amount +
                ", latitude=" + latitude +
                ", longitude=" + longitude +
                ", timestamp=" + timestamp +
                '}';
    }
}
