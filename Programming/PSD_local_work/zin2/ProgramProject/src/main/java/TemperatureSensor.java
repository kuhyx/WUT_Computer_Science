import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.source.SourceFunction;

import java.util.Random;

public class TemperatureSensor {

    public static void main(String[] args) throws Exception {
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        // Generating random temperature data
        DataStream<SensorReading> input = env.addSource(new SourceFunction<SensorReading>() {
            private boolean running = true;

            @Override
            public void run(SourceContext<SensorReading> ctx) throws Exception {
                Random rand = new Random();

                while (running) {
                    Thread.sleep(1000); // Sleep for a second before generating more data
                    ctx.collect(new SensorReading("sensor_1", rand.nextDouble() * 25 - 10));
                }
            }

            @Override
            public void cancel() {
                running = false;
            }
        });

        // Processing temperature data to find values below 0
        input
            .filter(reading -> reading.temperature < 0)
            .print();

        env.execute("Temperature Sensor Processing");
    }

    // Data type for sensor readings
    public static class SensorReading {
        public String sensorId;
        public double temperature;

        public SensorReading() {
        }

        public SensorReading(String sensorId, double temperature) {
            this.sensorId = sensorId;
            this.temperature = temperature;
        }
    }
}
