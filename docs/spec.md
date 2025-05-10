# 📜 R2R Protocol Specification

## 🧾 Overview

This document defines the **Robot-to-Robot (R2R) Communication Protocol**, a lightweight standard for structured communication between autonomous robotic agents.

## 📡 Message Format

All messages follow a consistent structure:

```json
{
  "header": {
    "version": "1.0",
    "timestamp": 1718000000,
    "source_id": "robot_001",
    "target_id": "robot_002"
  },
  "type": "status/task_request/task_response/command/negotiation/error",
  "payload": { ... }
}

```

## Header Fields

| Field     | Description                      |
|-----------|----------------------------------|
| version   | Protocol version (e.g., "1.0")   |
| timestamp | Unix timestamp (seconds)         |
| source_id | Unique ID of sending robot       |
| target_id | Optional: intended recipient     |


## Message Types

| Type          | Purpose                                          |
|---------------|--------------------------------------------------|
| status        | Health, battery, position, task progress         |
| task_request  | Request another robot to perform an action       |
| task_response | Accept/decline a task request                    |
| negotiation   | Used in collaborative task allocation            |
| command       | Direct control command from one robot to another |
| error         | Communicates errors during execution             |



## 💬 Example Use Cases

### 1. Status Broadcast

```json
{
  "header": {
    "version": "1.0",
    "timestamp": 1718000000,
    "source_id": "robot_001"
  },
  "type": "status",
  "payload": {
    "battery": 85,
    "position": {"x": 10.2, "y": 5.1},
    "task_progress": 0.75
  }
}
```

### 2. Task Request


```json

{
  "header": {
    "version": "1.0",
    "timestamp": 1718000001,
    "source_id": "bot_01",
    "target_id": "bot_02"
  },
  "type": "task_request",
  "payload": {
    "task_id": "T001",
    "description": "Pick up item at location (3.4, 6.7)",
    "deadline": 1718000100
  }
}
```

### 3. Task Response

```json 
{
  "header": {
    "version": "1.0",
    "timestamp": 1718000002,
    "source_id": "bot_02",
    "target_id": "bot_01"
  },
  "type": "task_response",
  "payload": {
    "task_id": "T001",
    "accepted": true,
    "estimated_time": 45
  }
}
```

## 🔐 Authentication (Optional)

Robots may authenticate each other using:

- Shared tokens

- Public-key cryptography

- TLS mutual authentication


## 🔄 Task Negotiation

Supports auction-style bidding or consensus-based task allocation.

Example negotiation payload:

```json 
{
  "type": "negotiation",
  "payload": {
    "task_id": "T002",
    "action": "bid",
    "cost": 30,
    "capabilities": ["arm", "camera"]
  }
}
```

## 📦 Transport Layer

Supported transports:

- TCP/IP
- UDP
- MQTT
- WebSocket
- ROS2 (optional integration)


## ⚠️ Error Handling

Standardized error codes:

| Code | Description             |
|------|-------------------------|
| 100  | Invalid message format  |
| 101  | Unknown target robot    |
| 102  | Task already assigned   |
| 103  | Unauthorized access     |
| 104  | Network timeout         |


## 🧱 Extension Mechanism

New message types and payloads can be added as long as they follow the base schema. Implementations should ignore unknown fields


## 📌 Future Roadmap

- Integration with ROS2
- Web interface for monitoring swarms
- Simulation support (Gazebo, Unity Robotics)
- Edge computing support (fleet-wide AI coordination)
- Enhanced security features for data transmission
- Improved error handling mechanisms


`








