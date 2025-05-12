
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

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


@dataclass
class NegotiationAction:
    """
    Represents a negotiation action, e.g., bid, propose, accept, reject.
    """
    task_id: str
    action: str  # e.g., "bid", "propose_task", "accept_task", "reject_task", "counter_offer"
    details: Dict[str, Any] = field(default_factory=dict) # e.g., {"cost": 30, "capabilities": ["arm", "camera"]} or {"reason": "unavailable"}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "action": self.action,
            "details": self.details,
        }

# You might also want a generic payload or ensure other specific payloads are defined
@dataclass
class GenericPayload:
    data: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return self.data

@dataclass
class Telemetry:
    data_points: Dict[str, Any] # e.g., {"temperature": 25.5, "speed": 1.2}

    def to_dict(self) -> Dict[str, Any]:
        return self.data_points

@dataclass
class CommandPayload:
    command_name: str
    args: List[Any] = field(default_factory=list)
    kwargs: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "command_name": self.command_name,
            "args": self.args,
            "kwargs": self.kwargs,
        }

