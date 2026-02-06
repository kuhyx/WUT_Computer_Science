package model;

public class TemperatureAlarm {
    private String thermometerId;
    private long timestamp;
    private double temperature;
    
    public TemperatureAlarm() {
    }
    
    public TemperatureAlarm(String thermometerId, long timestamp, double temperature) {
        this.thermometerId = thermometerId;
        this.timestamp = timestamp;
        this.temperature = temperature;
    }
    
    public String getThermometerId() {
        return thermometerId;
    }
    
    public void setThermometerId(String thermometerId) {
        this.thermometerId = thermometerId;
    }
    
    public long getTimestamp() {
        return timestamp;
    }
    
    public void setTimestamp(long timestamp) {
        this.timestamp = timestamp;
    }
    
    public double getTemperature() {
        return temperature;
    }
    
    public void setTemperature(double temperature) {
        this.temperature = temperature;
    }
}
