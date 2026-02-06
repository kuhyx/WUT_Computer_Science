from flask import Flask, jsonify
from confluent_kafka import Consumer, KafkaError

app = Flask(__name__)

@app.route('/alarms', methods=['GET'])
def get_alarms():
    alarms = []
    conf = {'bootstrap.servers': "localhost:9092",
            'group.id': "alarm_group",
            'auto.offset.reset': 'earliest'}

    consumer = Consumer(**conf)
    consumer.subscribe(['alarms'])

    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            break
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                return str(msg.error()), 500
        alarms.append(json.loads(msg.value().decode('utf-8')))
    
    consumer.close()
    return jsonify(alarms)

if __name__ == '__main__':
    app.run(debug=True)
