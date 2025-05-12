
# sdk/python/r2r_protocol/message_format.py

class Message:
    # ... definition of your Message class ...
    def __init__(self, message_id, message_type, sender_id, receiver_id, timestamp, payload):
        self.message_id = message_id
        self.message_type = message_type
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.timestamp = timestamp
        self.payload = payload
    # ... other methods ...

class MessageFormat:
    def __init__(self, message):
        self.message = message

    def format_message(self):
        formatted_message = {
            "message_id": self.message.message_id,
            "message_type": self.message.message_type,
            "sender_id": self.message.sender_id,
            "receiver_id": self.message.receiver_id,
            "timestamp": self.message.timestamp,
            "payload": self.message.payload
        }
        return formatted_message
    def parse_message(self, formatted_message):
        self.message.message_id = formatted_message.get("message_id")
        self.message.message_type = formatted_message.get("message_type")
        self.message.sender_id = formatted_message.get("sender_id")
        self.message.receiver_id = formatted_message.get("receiver_id")
        self.message.timestamp = formatted_message.get("timestamp")
        self.message.payload = formatted_message.get("payload")
    def validate_message(self):
        if not isinstance(self.message.message_id, int):
            raise ValueError("Invalid message_id: must be an integer")
        if not isinstance(self.message.message_type, str):
            raise ValueError("Invalid message_type: must be a string")
        if not isinstance(self.message.sender_id, str):
            raise ValueError("Invalid sender_id: must be a string")
        if not isinstance(self.message.receiver_id, str):
            raise ValueError("Invalid receiver_id: must be a string")
        if not isinstance(self.message.timestamp, str):
            raise ValueError("Invalid timestamp: must be a string")
        if not isinstance(self.message.payload, dict):
            raise ValueError("Invalid payload: must be a dictionary")
