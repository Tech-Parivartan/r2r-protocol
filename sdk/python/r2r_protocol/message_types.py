
from enum import Enum

class MessageType(Enum):
    """
    Defines the different types of messages that can be exchanged.
    """
    STATUS = "STATUS"
    COMMAND = "COMMAND"
    TELEMETRY = "TELEMETRY"
    LOG = "LOG"
    HEARTBEAT = "HEARTBEAT"
    # Add other message types as needed
