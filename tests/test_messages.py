import json
from r2r_protocol import RobotClient

def test_send_status():
    client = RobotClient(robot_id="test_bot", host="localhost", port=8080)
    client.send_status({
        "battery": 90,
        "position": {"x": 1.0, "y": 2.0},
        "task_progress": 0.5
    })
    print("Status sent.")
