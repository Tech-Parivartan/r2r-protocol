
import json
import socket
import time

class RobotClient:
    def __init__(self, robot_id, host="localhost", port=8080):
        self.robot_id = robot_id
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def send_status(self, status_data):
        msg = {
            "header": {
                "version": "1.0",
                "timestamp": int(time.time()),
                "source_id": self.robot_id
            },
            "type": "status",
            "payload": status_data
        }
        self._send(msg)

    def _send(self, msg):
        data = json.dumps(msg).encode("utf-8")
        self.sock.sendall(data)

    def listen(self):
        while True:
            data = self.sock.recv(4096)
            if not data:
                break
            yield json.loads(data.decode("utf-8"))

