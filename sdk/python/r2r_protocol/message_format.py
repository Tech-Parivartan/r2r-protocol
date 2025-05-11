
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

# Or if it's a Pydantic model or dataclass:
# from pydantic import BaseModel
# class Message(BaseModel):
#     