import socket
import json
import time

from typing import Any
from .message_types import MessageType
from .payloads import Status, NegotiationAction # Add NegotiationAction

class RobotClient:
    def __init__(self, robot_id, host="localhost", port=8080):
        self.robot_id = robot_id
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.message_version = "1.0" # Define message version

    def _send(self, msg_type: MessageType, payload: Any):
        """
        Internal method to construct and send a message.
        Payload should be an object with a to_dict() method.
        """
        message = {
            "header": {
                "version": self.message_version,
                "timestamp": int(time.time()),
                "source_id": self.robot_id
            },
            "type": msg_type.value, # Use MessageType enum value
            "payload": payload.to_dict() if hasattr(payload, 'to_dict') else payload
        }
        data = json.dumps(message).encode("utf-8")
        # Add a length prefix for robust message framing (optional but recommended)
        # For simplicity, sending raw JSON for now as per original _send
        self.sock.sendall(data)
        # Consider adding a delimiter or length prefix if not already handled by the server
        # For example, self.sock.sendall(data + b'\n') if server expects newline delimited JSON

    def send_status(self, status_payload: Status):
        """Sends a status update."""
        self._send(MessageType.STATUS, status_payload)

    def send_negotiation_action(self, negotiation_payload: NegotiationAction):
        """Sends a task negotiation action."""
        self._send(MessageType.NEGOTIATION, negotiation_payload)

    

    def listen(self):
        # Basic listening logic, needs robust message parsing (e.g., handling partial messages, delimiters)
        buffer = b""
        while True:
            try:
                data = self.sock.recv(4096)
                if not data:
                    print("Connection closed by server.")
                    break
                buffer += data
                # Assuming messages are newline-terminated JSON for this example
                # In a real scenario, you'd need a more robust framing mechanism
                while b'\n' in buffer:
                    message_data, buffer = buffer.split(b'\n', 1)
                    if message_data:
                        try:
                            message = json.loads(message_data.decode('utf-8'))
                            print(f"Received: {message}")
                            # Add message handling logic here based on message type
                            # e.g., if message['type'] == MessageType.COMMAND.value:
                            #    self.handle_command(message['payload'])
                        except json.JSONDecodeError:
                            print(f"Error decoding JSON: {message_data.decode('utf-8', errors='ignore')}")
                        except Exception as e:
                            print(f"Error processing message: {e}")
            except ConnectionResetError:
                print("Connection reset by peer.")
                break
            except Exception as e:
                print(f"Listening error: {e}")
                break
        self.close()

    def close(self):
        """Closes the socket connection."""
        if self.sock:
            self.sock.close()
            self.sock = None
            print(f"Connection closed for robot {self.robot_id}")


