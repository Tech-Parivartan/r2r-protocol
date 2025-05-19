# Chapter 5 : Robot client (Python SDK) :→

Welcome back, aspiring robot developers! In our journey so far, we've explored the fundamental concepts of the R2R Protocol: the overall idea of a universal robot language (Chapter 1: R2R Protocol), the standard structure of a Message (Chapter 2: Message), how Message Types categorize the purpose of a message, and how Payloads carry the specific data within that message.

Now, it's time to get practical! How does a *real robot* or a program controlling a robot *actually use* the R2R Protocol? This is where the **Robot Client (Python SDK)** comes in.

# **What is the Robot Client?**

Imagine your robot is a person who needs to talk on a very specific radio frequency using a very specific language (the R2R Protocol). They could try to build their own radio from scratch and learn the language rules word-for-word... or they could use a **specialized R2R walkie-talkie** that already knows how to do all of that!

The **Robot Client** from the R2R Protocol Python SDK is that specialized walkie-talkie (or, more accurately, a network adapter and translator). It's the primary tool you, as a developer, will use in your robot's code to make it speak and understand the R2R language.


![1_Chapter_5_Robot_Client_(Python_SDK)](./1_Chapter_5_Robot_Client_(Python_SDK).png)

The Robot Client handles the complex, repetitive tasks required by the protocol:

1. **Connecting:** Establishing a connection to other robots or a central R2R server over a network (like TCP/IP).
2. **Formatting (Sending):** Taking the data you want to send (like a status payload) and wrapping it correctly into a full R2R Message structure, then converting that structure into bytes suitable for sending over the network.
3. **Parsing (Receiving):** Receiving raw bytes from the network, converting them back into a structured R2R Message object, validating it, and making it available for your robot's application code to process.

Essentially, the `RobotClient` hides the low-level networking and message formatting/parsing details so you can focus on your robot's actual logic (moving, sensing, performing tasks) and its R2R communication *intent* (sending status, processing a command).

# **Your First Robot Client: Connecting**

To start communicating using R2R, your robot's program needs to create an instance of the `RobotClient`. This client needs to know who *it* is (`robot_id`) and where to connect (`host`, `port`).

Let's see how you create one:

```python
# Conceptual code for a robot program
from r2r_protocol import RobotClient

# Define connection details
MY_ROBOT_ID = "delivery_bot_42"
R2R_SERVER_HOST = "192.168.1.100" # IP address of the R2R server or another robot
R2R_SERVER_PORT = 8080         # Port the R2R service is listening on

# 1. Create an instance of the RobotClient
print(f"Attempting to connect as {MY_ROBOT_ID}...")
try:
    client = RobotClient(
        robot_id=MY_ROBOT_ID,
        host=R2R_SERVER_HOST,
        port=R2R_SERVER_PORT
    )
    print("Robot Client created and connected successfully!")

    # Now you can use the client to send and receive messages...

except ConnectionRefusedError:
    print(f"Connection failed: Server at {R2R_SERVER_HOST}:{R2R_SERVER_PORT} is not reachable or refused the connection.")
except Exception as e:
    print(f"An error occurred during connection: {e}")

# Remember to close the connection when done
# client.close()
```

This simple code creates the `client` object. When you create the `RobotClient`, it immediately tries to establish a connection to the specified host and port. If successful, you have a working connection through which R2R messages can flow. The `robot_id` you provide will be automatically included in the `sender_id` field of every message this client sends.

# **Sending Messages with the Client**

Once connected, sending a message is straightforward. The `RobotClient` provides methods to help you send specific types of messages.

Let's revisit our Delivery Robot #001 sending a status update, now using the actual `RobotClient`. We know from Chapter 3: Message Types and Chapter 4: Payloads that a status update uses the `STATUS` type and requires a specific Payload structure (using the `Status` class).

Here's how the robot would use the client to send its status:

```python
# Conceptual code for a robot program (continuing from connection)
from r2r_protocol import RobotClient, MessageType
from r2r_protocol.payloads import Status # Import the Status payload class

# Assume 'client' is a connected RobotClient instance from the previous step

print(f"{client.robot_id}: Preparing status update...")

# 1. Create the specific payload data using the Status class
status_payload_data = Status(
    status="moving", # Set the main status string
    details={ # Add specific details in the details dictionary
        "battery_level": 15,
        "position": {"x": 10.2, "y": 5.1},
        "task": "delivering package"
    }
)

print(f"  Payload created: {status_payload_data.to_dict()}")

# 2. Use the client's helper method to send the status message
# The send_status method internally handles the message type (STATUS)
# and formatting the payload.
print(f"{client.robot_id}: Sending status message...")
try:
    client.send_status(status_payload_data)
    print(f"{client.robot_id}: Status message sent!")

except Exception as e:
    print(f"{client.robot_id}: Error sending message: {e}")

# When done, close the connection
# client.close()
```

The `client.send_status()` method is a convenience wrapper. It takes the `Status` object (which holds the Payload data), tells the client that this is a `STATUS` message, and triggers the internal sending process. This internal process (which we'll look at next) builds the complete R2R Message structure and sends it over the network.

Similarly, if the robot needed to send a command, it would prepare a `CommandPayload` and potentially use a `client.send_command()` method (if available, or a generic send method).

# **Receiving Messages with the Client**

The `RobotClient` also handles listening for incoming data from the network. When it receives data, it parses it back into the structured R2R Message format (specifically, a Python dictionary representing the message) and typically makes it available through a listening method or by triggering a callback function in your robot's code.

Here's a simplified look at how a robot might listen for and handle incoming messages:

```python
# Conceptual code for a robot program (receiving part)
from r2r_protocol import RobotClient, MessageType
# Assume other imports and client connection setup are done

# Assume 'client' is a connected RobotClient instance

print(f"{client.robot_id}: Starting to listen for incoming messages...")

# The client's listen() method blocks and processes incoming messages
# In a real application, this would likely run in a separate thread or loop
# that integrates with the robot's main control system.

# Conceptual simple listening loop provided by the SDK:
# (The actual implementation in client.py is a basic example
# that just prints, more complex handling would replace the print)
# client.listen()

# --- Example of what your code *might* do when the client receives a message ---
# Imagine the client's internal listener calls a function like this
def handle_incoming_message(message_dict):
    """
    This function is called by the client's listening mechanism
    whenever a complete R2R message is received and parsed.
    'message_dict' is the Python dictionary representing the message.
    """
    print(f"\n{client.robot_id}: Received a message!")
    print(f"  Sender: {message_dict.get('header', {}).get('source_id')}")
    print(f"  Type: {message_dict.get('type')}")
    print(f"  Payload: {message_dict.get('payload')}")

    # --- Process the message based on its type ---
    msg_type_str = message_dict.get('type')
    payload_dict = message_dict.get('payload', {})

    if msg_type_str == MessageType.COMMAND.value:
        print(f"\n{client.robot_id}: It's a COMMAND message!")
        command_name = payload_dict.get("command_name")
        args = payload_dict.get("args", [])
        kwargs = payload_dict.get("kwargs", {})
        print(f"  Executing command: {command_name} with args={args}, kwargs={kwargs}")
        # --- Your robot's logic to perform the command goes here ---
        if command_name == "go_to":
            if args:
                destination = args[0] # Assume first arg is destination
                print(f"    Moving to {destination}...")
                # Add robot's movement code
            else:
                 print("    Go_to command received without destination!")
        # ... handle other commands ...

    elif msg_type_str == MessageType.STATUS.value:
        print(f"\n{client.robot_id}: It's a STATUS message!")
        status_str = payload_dict.get("status")
        details = payload_dict.get("details", {})
        battery = details.get("battery_level")
        print(f"  Received status: {status_str}, Battery: {battery}%")
        # --- Your robot's logic to process status goes here ---
        # e.g., Update internal state of other robots

    # ... handle other message types (TELEMETRY, ERROR, etc.) ...

    else:
        print(f"\n{client.robot_id}: Received message of unhandled type: {msg_type_str}")

# To make the client use this handler, you would typically pass it during setup
# or have the client emit events that your code listens to.
# The current simple client.listen() just prints, but a more advanced version
# would integrate with your main robot loop or an event handler.

# To keep a robot program running and listening, you might do something like:
# while True:
#    client.listen_for_one_message() # Conceptual method
#    process_message(received_message)
# Or run client.listen() in a separate thread.
```

This conceptual `handle_incoming_message` function shows how your code interacts with the data provided by the `RobotClient`. The client takes care of receiving and parsing the raw data, and your code then reads the `type` and `payload` from the resulting dictionary to decide what action to take, just as we discussed in previous chapters.

# **How the Robot Client Works Under the Hood (Simplified)**

Let's peek inside the `RobotClient` to see how it handles the sending process we just used with `client.send_status()`.

When you call a method like `client.send_status(status_payload_data)`, here's a simplified flow:


![2_Chapter_5_Robot_Client_(Python_SDK)](./2_Chapter_5_Robot_Client_(Python_SDK).png)

This diagram illustrates how your high-level call to `send_status` translates into the client building the complete R2R Message structure as a Python dictionary and then serializing it into bytes using the `json` library before sending it over the network connection (`sock`).

Let's look at a simplified snippet from the `RobotClient`'s `_send` method (from `sdk/python/r2r_protocol/client.py`) to see this in code:

```python
# Snippet from sdk/python/r2r_protocol/client.py (simplified)
import json
import time
from typing import Any
from .message_types import MessageType # Uses the MessageType Enum

class RobotClient:
    # ... __init__ and other methods ...

    def _send(self, msg_type: MessageType, payload: Any):
        """
        Internal method to construct and send a message.
        Payload should typically be an object with a to_dict() method.
        """
        # 1. Build the full Message structure as a Python dictionary
        message_dict = {
            "header": {
                "version": self.message_version, # e.g., "1.0"
                "timestamp": int(time.time()),   # Current time
                "source_id": self.robot_id       # The robot's ID
            },
            "type": msg_type.value, # Get the string value from the MessageType enum
            # 2. Get the payload data - call to_dict() if available, otherwise use as is
            "payload": payload.to_dict() if hasattr(payload, 'to_dict') else payload
        }

        # 3. Convert the Python dictionary into a JSON string (bytes)
        data_to_send = json.dumps(message_dict).encode("utf-8")

        # 4. Send the bytes over the network socket
        # self.sock.sendall(data_to_send)
        # Note: Real-world might add length prefix or delimiter for robust framing!
        # Example adding newline delimiter:
        self.sock.sendall(data_to_send + b'\n') # Assuming receiver handles newline delimiter
```

This snippet shows the core steps: creating the Python dictionary `message_dict` with the standard R2R fields (`header`, `type`, `payload`), converting it to JSON bytes, and sending it via the socket. The `send_status` method (and other similar helper methods) simply calls `_send` with the correct `MessageType` and your provided payload object.

On the receiving side, the `client.listen()` method (or its underlying logic) handles the reverse: receiving bytes, buffering them until a complete message is available (e.g., ending in `b'\n'`), parsing the JSON bytes back into a Python dictionary, and then providing that dictionary to your robot's handling code. The parsing step uses `json.loads()`:

```python
# Snippet from sdk/python/r2r_protocol/client.py (simplified listening part)
import json

class RobotClient:
    # ... __init__, _send, send_status, etc. ...

    def listen(self):
        buffer = b""
        print(f"{self.robot_id}: Listening...")
        while True:
            try:
                data = self.sock.recv(4096) # Receive bytes from the socket
                if not data:
                    print("Connection closed by server.")
                    break
                buffer += data # Add received data to buffer

                # --- Simplified message framing assuming newline delimiter ---
                while b'\n' in buffer:
                    message_data_bytes, buffer = buffer.split(b'\n', 1) # Split buffer at newline
                    if message_data_bytes:
                        try:
                            # 1. Decode bytes to string
                            message_data_str = message_data_bytes.decode('utf-8')
                            # 2. Parse JSON string into a Python dictionary
                            received_message_dict = json.loads(message_data_str)
                            # 3. Provide the dictionary to your application logic
                            # --- In a real app, this would call YOUR handler ---
                            # Example: self.handle_incoming_message(received_message_dict)
                            print(f"[{self.robot_id}] Received & Parsed: {received_message_dict}") # Simple print for demo
                            # --- Your code would now process received_message_dict ---

                        except json.JSONDecodeError:
                            print(f"[{self.robot_id}] Error decoding JSON: {message_data_str}")
                        except Exception as e:
                            print(f"[{self.robot_id}] Error processing message: {e}")
            except Exception as e:
                print(f"[{self.robot_id}] Listening error: {e}")
                break
        self.close() # Close connection on error or disconnect
```

This listening snippet shows the use of `json.loads()` to turn the received JSON string back into a Python dictionary, which is then ready for your robot's code to inspect the type and payload.

# **Conclusion**

The **Robot Client (Python SDK)** is the essential tool for implementing the R2R Protocol in your Python-based robots. It abstracts away the complexities of network communication (connecting, sending/receiving bytes) and protocol formatting (building the full Message structure, serializing/deserializing JSON). By using the `RobotClient`, you can focus on defining your robot's unique behavior and its R2R communication intent using standardized Message Types and Payloads, letting the SDK handle the low-level details.

We've seen how to create a client, send a status message using a helper method that leverages the underlying `_send` mechanism, and conceptually understand how receiving and parsing works.

Now that we understand how a single robot uses the SDK to communicate, you might be wondering how the development and deployment process for such a protocol and its SDK is managed. That's where Continuous Integration/Continuous Deployment (CI/CD) comes in!

Ready to learn about ensuring the quality and smooth release of the R2R Protocol SDK itself? Let's move on to Chapter 6: CI/CD (GitHub Actions)!



