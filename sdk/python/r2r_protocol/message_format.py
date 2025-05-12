
# # sdk/python/r2r_protocol/message_format.py

# class Message:
#     # ... definition of your Message class ...
#     def __init__(self, message_id, message_type, sender_id, receiver_id, timestamp, payload):
#         self.message_id = message_id
#         self.message_type = message_type
#         self.sender_id = sender_id
#         self.receiver_id = receiver_id
#         self.timestamp = timestamp
#         self.payload = payload
#     # ... other methods ...

# # Or if it's a Pydantic model or dataclass:
# # from pydantic import BaseModel
# # class Message(BaseModel):
# #    

# filepath: sdk/python/r2r_protocol/message_format.py

class Header:
    def __init__(self, version: str, timestamp: int, source_id: str, target_id: str = None):
        self.version = version
        self.timestamp = timestamp
        self.source_id = source_id
        self.target_id = target_id

    def to_dict(self):
        data = {
            "version": self.version,
            "timestamp": self.timestamp,
            "source_id": self.source_id,
        }
        if self.target_id:
            data["target_id"] = self.target_id
        return data 