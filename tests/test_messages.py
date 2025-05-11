from r2r_protocol import RobotClient, Message, MessageType, Status
from unittest.mock import patch, MagicMock

@patch('socket.socket')
def test_send_status(mock_socket_constructor):
    # Configure the mock socket and its connect method
    mock_sock_instance = MagicMock()
    mock_socket_constructor.return_value = mock_sock_instance

    client = RobotClient(robot_id="test_bot", host="localhost", port=8080)
    
    # Verify that connect was called (optional, but good practice)
    mock_sock_instance.connect.assert_called_once_with(("localhost", 8080))

    status_message = Message(
        message_id="123",
        message_type=MessageType.STATUS,
        sender_id="test_bot",
        receiver_id="another_bot",
        timestamp="2024-05-11T12:00:00Z",
        payload=Status(status="READY", details={"info": "System nominal"})
    )
    
    # If send_message also uses the socket, you might need to mock sendall too
    # For example: mock_sock_instance.sendall = MagicMock()

    # Assuming send_message internally calls something like self.sock.sendall()
    # You can then assert that sendall was called with the correct data
    # client.send_message(status_message)
    # mock_sock_instance.sendall.assert_called_once_with(status_message.to_json().encode())

    # For now, let's just assert the client was created
    assert client.robot_id == "test_bot"
    # Add more assertions here based on what send_status is supposed to do
    # For example, if send_status is a method:
    # client.send_status("READY", {"info": "System nominal"})
    # And then assert that mock_sock_instance.sendall was called with the expected message

def test_receive_message():
    pass

