package com.anomaly.producer;

import com.anomaly.generator.TransactionGenerator;
import com.anomaly.model.Transaction;
import com.google.gson.Gson;
import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.StringSerializer;

import java.util.*;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ThreadLocalRandom;

public class TransactionProducer {
    //private static final Logger logger = LoggerFactory.getLogger(TransactionProducer.class);
    private static final String BOOTSTRAP_SERVERS = "localhost:9092";
    private static final String TOPIC_NAME = "transactions";
    private static final TransactionGenerator generator = new TransactionGenerator();
    private static final Gson gson = new Gson();

    public static void main(String[] args) {
        // Create producer properties
        Properties properties = new Properties();
        properties.setProperty(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, BOOTSTRAP_SERVERS);
        properties.setProperty(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        properties.setProperty(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());

        // Create producer
        KafkaProducer<String, String> producer = new KafkaProducer<>(properties);

        // Add shutdown hook
        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            //logger.info("Shutting down producer...");
            producer.flush();
            producer.close();
            //logger.info("Producer closed");
        }));

        // Generate and send transactions
        try {
            while (true) {
                // Normal transaction generation
                if (ThreadLocalRandom.current().nextDouble() < 0.05) {
                    // 5% chance to generate a frequency anomaly
                    List<Transaction> anomalousTransactions = generator.generateFrequencyAnomaly(null);
                    for (Transaction transaction : anomalousTransactions) {
                        sendTransaction(producer, transaction);
                    }
                } else {
                    // Regular transaction
                    boolean forceAnomaly = ThreadLocalRandom.current().nextDouble() < 0.02; // 2% chance
                    Transaction transaction = generator.generateTransaction(forceAnomaly, -1);
                    sendTransaction(producer, transaction);
                }

                // Sleep between 100ms and 1s before generating next transaction
                Thread.sleep(ThreadLocalRandom.current().nextLong(100, 1000));
            }
        } catch (InterruptedException | ExecutionException e) {
            //logger.error("Error in transaction producer", e);
        } finally {
            producer.flush();
            producer.close();
        }
    }

    private static void sendTransaction(KafkaProducer<String, String> producer, Transaction transaction)
            throws ExecutionException, InterruptedException {
        String jsonTransaction = gson.toJson(transaction);
        ProducerRecord<String, String> record = new ProducerRecord<>(
                TOPIC_NAME,
                transaction.getCardId(),
                jsonTransaction
        );

        producer.send(record, (metadata, exception) -> {
            if (exception == null) {
                //logger.info("Received metadata: Topic: {}, Partition: {}, Offset: {}, Timestamp: {}",
                //        metadata.topic(), metadata.partition(), metadata.offset(), metadata.timestamp());
            } else {
                //logger.error("Error sending message", exception);
            }
        }).get(); // Making it synchronous for demonstration
    }
}
