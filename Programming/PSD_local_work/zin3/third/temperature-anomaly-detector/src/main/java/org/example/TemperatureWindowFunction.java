package org.example;

import org.apache.flink.api.java.tuple.Tuple;
import org.apache.flink.streaming.api.functions.windowing.WindowFunction;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;
import org.example.TemperatureAnomalyDetector.TemperatureReading;
import org.example.TemperatureAnomalyDetector.TemperatureAlert;

import java.util.Iterator;

public class TemperatureWindowFunction implements WindowFunction<TemperatureReading, TemperatureAlert, String, TimeWindow> {
    
    @Override
    public void apply(
            String key, 
            TimeWindow window, 
            Iterable<TemperatureReading> values, 
            Collector<TemperatureAlert> out) {
        
        Iterator<TemperatureReading> iterator = values.iterator();
        if (!iterator.hasNext()) {
            return; // No readings in this window
        }
        
        // Find the lowest temperature in the window
        TemperatureReading lowestReading = iterator.next();
        double lowestTemp = lowestReading.temperature;
        
        while (iterator.hasNext()) {
            TemperatureReading reading = iterator.next();
            if (reading.temperature < lowestTemp) {
                lowestTemp = reading.temperature;
                lowestReading = reading;
            }
        }
        
        // Create and emit an alert for the lowest temperature reading
        String message = String.format("Freezing temperature alert! %s reported %.2f°C", 
                lowestReading.thermometerId, lowestTemp);
        
        TemperatureAlert alert = new TemperatureAlert(
                lowestReading.thermometerId, 
                lowestTemp, 
                message
        );
        
        out.collect(alert);
    }
}
