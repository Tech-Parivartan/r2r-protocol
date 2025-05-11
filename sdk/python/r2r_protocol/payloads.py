
from typing import Dict, Any

class Status:
    """
    Represents the payload for a STATUS message.
    """
    def __init__(self, status: str, details: Dict[str, Any] = None):
        self.status = status
        self.details = details if details is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "details": self.details
        }

class Command:
    """
    Represents the payload for a COMMAND message.
    """
    def __init__(self, command_name: str, parameters: Dict[str, Any] = None):
        self.command_name = command_name
        self.parameters = parameters if parameters is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "command_name": self.command_name,
            "parameters": self.parameters
        }

# Add other payload classes as needed (e.g., Telemetry, Log)

