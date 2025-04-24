import json
import threading
import tkinter as tk
from tkinter import ttk
from confluent_kafka import Consumer
import sys
import os
from datetime import datetime
from collections import Counter

# Add parent directory to path to import model
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model.temperature_alarm import TemperatureAlarm

class AlarmVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Temperature Alarm Visualizer")
        self.root.geometry("600x400")
        
        # Create the list model for alarms
        self.alarm_list = tk.Listbox(root, font=("Courier", 12))
        self.alarm_list.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollbar
        scrollbar = ttk.Scrollbar(self.alarm_list, orient="vertical", command=self.alarm_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.alarm_list.config(yscrollcommand=scrollbar.set)
        
        # Create stats panel
        self.stats_frame = tk.Frame(root)
        self.stats_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.stats_label = tk.Label(self.stats_frame, text="No alarms yet")
        self.stats_label.pack(pady=5)
        
        # Stats tracking
        self.thermometer_alarm_count = Counter()
        self.max_alarms = 100
        
        # Start Kafka consumer in a separate thread
        self.consumer_thread = threading.Thread(target=self.consume_alarms, daemon=True)
        self.consumer_thread.start()
    
    def consume_alarms(self):
        # Set up Kafka consumer with confluent-kafka
        consumer_config = {
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'alarm-visualizer',
            'auto.offset.reset': 'latest'
        }
        consumer = Consumer(consumer_config)
        consumer.subscribe(['Alarm'])
        
        try:
            while True:
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    print(f"Consumer error: {msg.error()}")
                    continue
                    
                # Parse the alarm message
                alarm_data = json.loads(msg.value().decode('utf-8'))
                alarm = TemperatureAlarm.from_dict(alarm_data)
                
                # Format the timestamp
                timestamp_dt = datetime.fromtimestamp(alarm.timestamp / 1000)
                formatted_date = timestamp_dt.strftime('%Y-%m-%d %H:%M:%S')
                
                # Create alarm message
                alarm_message = f"⚠️ ALARM: Thermometer {alarm.thermometer_id} reported {alarm.temperature:.2f}°C at {formatted_date}"
                
                # Update the UI
                self.root.after(0, self.update_ui, alarm_message, alarm.thermometer_id)
                
        except Exception as e:
            print(f"Error in Kafka consumer: {e}")
        finally:
            consumer.close()
    
    def update_ui(self, alarm_message, thermometer_id):
        # Add new alarm to the top of the list
        self.alarm_list.insert(0, alarm_message)
        
        # Keep list at a reasonable size
        if self.alarm_list.size() > self.max_alarms:
            self.alarm_list.delete(self.max_alarms)
        
        # Update statistics
        self.thermometer_alarm_count[thermometer_id] += 1
        
        # Format stats string
        if self.thermometer_alarm_count:
            stats_parts = [f"{id}={count}" for id, count in self.thermometer_alarm_count.items()]
            stats_text = "Alarm Counts: " + ", ".join(stats_parts)
            self.stats_label.config(text=stats_text)

def main():
    root = tk.Tk()
    app = AlarmVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
