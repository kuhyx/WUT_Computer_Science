package com.anomaly.model;

import java.time.Instant;

public class TransactionAlert {
    private String alertType;
    private String cardId;
    private String userId;
    private double amount;
    private double latitude;
    private double longitude;
    private Instant timestamp;
    private String message;
    private Instant alertTime;

    public TransactionAlert() {
        this.alertTime = Instant.now();
    }

    public TransactionAlert(String alertType, String cardId, String userId, double amount,
                           double latitude, double longitude, Instant timestamp, String message) {
        this.alertType = alertType;
        this.cardId = cardId;
        this.userId = userId;
        this.amount = amount;
        this.latitude = latitude;
        this.longitude = longitude;
        this.timestamp = timestamp;
        this.message = message;
        this.alertTime = Instant.now();
    }

    // Getters and setters
    public String getAlertType() { return alertType; }
    public void setAlertType(String alertType) { this.alertType = alertType; }
    public String getCardId() { return cardId; }
    public void setCardId(String cardId) { this.cardId = cardId; }
    public String getUserId() { return userId; }
    public void setUserId(String userId) { this.userId = userId; }
    public double getAmount() { return amount; }
    public void setAmount(double amount) { this.amount = amount; }
    public double getLatitude() { return latitude; }
    public void setLatitude(double latitude) { this.latitude = latitude; }
    public double getLongitude() { return longitude; }
    public void setLongitude(double longitude) { this.longitude = longitude; }
    public Instant getTimestamp() { return timestamp; }
    public void setTimestamp(Instant timestamp) { this.timestamp = timestamp; }
    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }
    public Instant getAlertTime() { return alertTime; }
    public void setAlertTime(Instant alertTime) { this.alertTime = alertTime; }

    @Override
    public String toString() {
        return "TransactionAlert{" +
                "alertType='" + alertType + '\'' +
                ", cardId='" + cardId + '\'' +
                ", userId='" + userId + '\'' +
                ", amount=" + amount +
                ", latitude=" + latitude +
                ", longitude=" + longitude +
                ", message='" + message + '\'' +
                ", alertTime=" + alertTime +
                '}';
    }
}
