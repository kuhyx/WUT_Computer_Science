package com.anomaly.model;

import java.time.Instant;

public class TransactionAlert {
    private String alertType;
    private Instant alertTime;
    private Instant timestamp;
    private String cardId;
    private String userId;
    private double amount;
    private double latitude;
    private double longitude;
    private String message;

    // Default constructor for Gson deserialization
    public TransactionAlert() {
    }
    
    public TransactionAlert(String alertType, Instant alertTime, Instant timestamp, 
                           String cardId, String userId, double amount, 
                           double latitude, double longitude, String message) {
        this.alertType = alertType;
        this.alertTime = alertTime;
        this.timestamp = timestamp;
        this.cardId = cardId;
        this.userId = userId;
        this.amount = amount;
        this.latitude = latitude;
        this.longitude = longitude;
        this.message = message;
    }

    // Getters and setters
    public String getAlertType() {
        return alertType;
    }

    public void setAlertType(String alertType) {
        this.alertType = alertType;
    }

    public Instant getAlertTime() {
        return alertTime;
    }

    public void setAlertTime(Instant alertTime) {
        this.alertTime = alertTime;
    }

    public Instant getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Instant timestamp) {
        this.timestamp = timestamp;
    }

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

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }
}
