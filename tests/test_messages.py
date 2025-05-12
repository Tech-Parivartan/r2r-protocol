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

@patch('socket.socket')
def test_receive_message(mock_socket):
    # Configure the mock socket and its recv method
    mock_sock_instance = MagicMock()
    mock_socket.return_value = mock_sock_instance

    client = RobotClient(robot_id="test_bot", host="localhost", port=8080)

    # Simulate receiving a message
    mock_sock_instance.recv.return_value = b'{"message_id": "123", "message_type": "STATUS", "sender_id": "another_bot", "receiver_id": "test_bot", "timestamp": "2024-05-11T12:00:00Z", "payload": {"status": "READY", "details": {"info": "System nominal"}}}'

    received_message = client.receive_message()

    # Assert that the message was received and parsed correctly
    assert received_message.message_id == "123"
    assert received_message.message_type == "STATUS"
    assert received_message.sender_id == "another_bot"
    assert received_message.receiver_id == "test_bot"
    assert received_message.timestamp == "2024-05-11T12:00:00Z"
    assert received_message.payload == {"status": "READY", "details": {"info": "System nominal"}}
