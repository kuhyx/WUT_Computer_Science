package com.anomaly.model;

/**
 * Represents a financial transaction with amount and available credit limit information.
 */
public class Transaction {
    private double amount;
    private double availableLimit;
    private String cardNumber;
    private String timestamp;

    // Default constructor for deserialization
    public Transaction() {
    }

    // Full constructor
    public Transaction(double amount, double availableLimit, String cardNumber, String timestamp) {
        this.amount = amount;
        this.availableLimit = availableLimit;
        this.cardNumber = cardNumber;
        this.timestamp = timestamp;
    }

    public double getAmount() {
        return amount;
    }

    public void setAmount(double amount) {
        this.amount = amount;
    }

    public double getAvailableLimit() {
        return availableLimit;
    }

    public void setAvailableLimit(double availableLimit) {
        this.availableLimit = availableLimit;
    }

    public String getCardNumber() {
        return cardNumber;
    }

    public void setCardNumber(String cardNumber) {
        this.cardNumber = cardNumber;
    }

    public String getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(String timestamp) {
        this.timestamp = timestamp;
    }

    @Override
    public String toString() {
        return "Transaction{" +
                "amount=" + amount +
                ", availableLimit=" + availableLimit +
                ", cardNumber='" + cardNumber + '\'' +
                ", timestamp='" + timestamp + '\'' +
                '}';
    }
}
