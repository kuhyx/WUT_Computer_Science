class TemperatureAlarm:
    def __init__(self, thermometer_id=None, timestamp=None, temperature=None):
        self.thermometer_id = thermometer_id
        self.timestamp = timestamp
        self.temperature = temperature
    
    def to_dict(self):
        return {
            "thermometerId": self.thermometer_id,
            "timestamp": self.timestamp,
            "temperature": self.temperature
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            thermometer_id=data.get("thermometerId"),
            timestamp=data.get("timestamp"),
            temperature=data.get("temperature")
        )
