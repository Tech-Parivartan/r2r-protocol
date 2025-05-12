
from enum import Enum

class MessageType(Enum):
    """
    Defines the different types of messages that can be exchanged.
    """
    
    HANDSHAKE = "handshake"
    HANDSHAKE_ACK = "handshake_ack"
    COMMAND = "command"
    STATUS = "status"
    TELEMETRY = "telemetry"
    ERROR = "error"
    HEARTBEAT = "heartbeat"
    
    NEGOTIATION = "negotiation"
    # Add other message types as needed
    
